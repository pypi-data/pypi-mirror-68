import json

from datetime import datetime
from itertools import chain

from py42.response import Py42Response
from py42.sdk.queries.query_filter import FilterGroup
from py42.sdk.queries.fileevents.file_event_query import FileEventQuery
from py42.sdk.queries.fileevents.filters import InsertionTimestamp
from py42.sdk.queries.alerts.alert_query import AlertQuery
from py42.sdk.queries.alerts.filters.alert_filter import DateObserved

from c42eventextractor.compat import str
from c42eventextractor.common import convert_datetime_to_timestamp, IncompatibleFilterError

_MAX_PAGE_SIZE = 10000
_TIMESTAMP_PRECISION = 0.001
FILTER_ERROR = u"{} filter can't be used with {} when a cursor checkpoint exists."


class BaseExtractor(object):

    _previous_event_count = _MAX_PAGE_SIZE

    def __init__(self, key, search_function, handlers, timestamp_filter, query_class):
        self._key = key
        self._search = search_function
        self._handlers = handlers
        self._timestamp_filter = timestamp_filter
        self._sort_key = timestamp_filter._term
        self._query_class = query_class

    def extract(self, *args):
        """Queries for recent events and keeps track of last event timestamp for future filtering.

        Passes the raw response from the py42 call to `handlers.handle_response`.
        The default implementation of `handlers.handle_response` prints to the
        console. Provide your own implementation for `handlers.handle_response` to do something
        else. Makes subsequent calls to py42 and `handlers.handle_response` if the total event
        count is greater than 10,000.

        The last event timestamp cursor is retrieved and stored using the respective
        `handlers.get_cursor_position` and `handlers.record_cursor_position` methods. The default
        implementation stores it in memory. Provide your own implementation of those methods to
        persist the cursor between runs.

        Args:
            *args: Additional query filter groups. Note: Throws an exception if it receives the
                same timestamp filter used by the extractor to keep track of cursor position and
                a cursor checkpoint is stored.
        """
        filter_groups = list(args)
        cursor_position = self._handlers.get_cursor_position()
        self._verify_filter_groups(filter_groups, cursor_position)
        self._extract_all(filter_groups)

    def extract_advanced(self, query):
        try:
            response = self._search(query)
            return self._handle_response(response)
        except Exception as ex:
            self._handlers.handle_error(ex)

    def _verify_filter_groups(self, filter_groups, cursor_position):
        if not all(isinstance(group, FilterGroup) for group in filter_groups):
            raise ValueError(
                u"arguments must be py42.sdk.queries.query_filter.FilterGroup objects."
            )

        filters = chain.from_iterable(
            json.loads(str(group)).get(u"filters") for group in filter_groups
        )
        if cursor_position and any(f.get(u"term") == self._timestamp_filter._term for f in filters):
            raise IncompatibleFilterError(
                FILTER_ERROR.format(self._timestamp_filter.__name__, self.__class__.__name__)
            )

    def _extract_all(self, filter_groups):
        if self._previous_event_count < _MAX_PAGE_SIZE:
            return

        original_filters = list(filter_groups)
        cursor_position = self._handlers.get_cursor_position()

        if cursor_position:
            self._add_timestamp_filter(filter_groups, cursor_position)

        query = self._create_query_from_filters(filter_groups)

        # do not recurse if handler returns no cursor
        if self.extract_advanced(query) and self._handlers.get_cursor_position():
            self._extract_all(original_filters)

    def _add_timestamp_filter(self, filter_groups, cursor_position):
        timestamp_filter = self._timestamp_filter.on_or_after(cursor_position)
        filter_groups.append(timestamp_filter)

    def _create_query_from_filters(self, filter_groups):
        query = self._query_class(*filter_groups)
        query.sort_direction = u"asc"
        query.sort_key = self._sort_key
        query.page_size = _MAX_PAGE_SIZE
        return query

    def _get_results_from_response(self, response):
        return response[self._key]

    def _handle_response(self, response):
        results = self._get_results_from_response(response)
        if results and self._timestamp_filter._term in results[-1]:
            timestamp, index = self._extract_timestamp_from_results(results)
            self._record_count(response)
            if index and self._previous_event_count >= _MAX_PAGE_SIZE:
                # truncate responses with the highest timestamp to avoid duplicates
                response._data_root[self._key] = response[self._key][:index]
            else:
                # either this is the last page, OR
                # every item on this page had the same timestamp.
                # increase the timestamp by .001 and continue
                timestamp += _TIMESTAMP_PRECISION

            self._handlers.handle_response(response)
            self._record_checkpoint(timestamp)
            return response

    def _extract_timestamp_from_results(self, results):
        """Return the highest timestamp found by the query and its index.
         This info is used to continue finding results without recording any duplicates.
        """
        index = self._get_index_where_truncation_begins(results)
        highest_timestamp = self._get_timestamp_from_item(results[index])

        return highest_timestamp, index

    def _get_index_where_truncation_begins(self, results):
        current_index = 0
        index = 0
        cutoff = self._get_timestamp_from_item(results[-1])
        results = results[:-1]
        for result in reversed(results):
            current_index -= 1
            next_most_recent = self._get_timestamp_from_item(result)
            if next_most_recent < cutoff:
                index = current_index
                break
        return index

    def _record_checkpoint(self, timestamp):
        if timestamp is not None:
            self._handlers.record_cursor_position(timestamp)

    def _record_count(self, response):
        count = response._data_root.get(u"totalCount", 0)
        self._previous_event_count = count

    def _get_timestamp_from_item(self, item):
        raise NotImplementedError


class AlertExtractor(BaseExtractor):
    def __init__(self, sdk, handlers):
        super(AlertExtractor, self).__init__(
            key=u"alerts",
            search_function=sdk.alerts.search,
            handlers=handlers,
            timestamp_filter=DateObserved,
            query_class=AlertQuery,
        )
        self._sort_key = u"CreatedAt"

    def _get_timestamp_from_item(self, item):
        date_observed_str = item[self._timestamp_filter._term]
        date_observed_str = date_observed_str[:25]  # remove nanoseconds
        date_observed = datetime.strptime(date_observed_str, u"%Y-%m-%dT%H:%M:%S.%f")
        date_observed_timestamp = convert_datetime_to_timestamp(date_observed)
        return date_observed_timestamp


class FileEventExtractor(BaseExtractor):
    def __init__(self, sdk, handlers):
        super(FileEventExtractor, self).__init__(
            key=u"fileEvents",
            search_function=sdk.securitydata.search_file_events,
            handlers=handlers,
            timestamp_filter=InsertionTimestamp,
            query_class=FileEventQuery,
        )

    def _get_timestamp_from_item(self, item):
        time_str = item[self._timestamp_filter._term]
        dt = datetime.strptime(time_str, u"%Y-%m-%dT%H:%M:%S.%fZ")
        timestamp = convert_datetime_to_timestamp(dt)
        return timestamp
