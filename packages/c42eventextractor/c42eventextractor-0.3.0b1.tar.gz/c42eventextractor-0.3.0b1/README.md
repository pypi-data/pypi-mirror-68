# c42eventextractor - Utilities to extract and record Code42 security events

![Build status](https://github.com/code42/security-event-extractor/workflows/build/badge.svg)
[![versions](https://img.shields.io/pypi/pyversions/c42eventextractor.svg)](https://pypi.org/project/c42eventextractor/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The `c42eventextractor` package provides modules that assist in the retrieval and logging of Code42 security events.
This is done by exposing handlers that allow developers to supply custom behaviors to occur when events are retrieved.
By default, the extractors will simply print their results to stdout, but these handlers can be extended to allow developers
to record the event info to whatever location or format they desire.

## Requirements

- Python 2.7.x or 3.5.0+
- Code42 Server 6.8.x+
- py42 version 1.0.1+

## Installation

Install `c42eventextractor` using pip:

```bash
pip install c42eventextractor
```

Or clone this repo and install manually:

```bash
python setup.py install
```


## Usage - Code42 Security Events

To get all security events, use the `FileEventExtractor`:

```python
from c42eventextractor.extractors import FileEventExtractor
from c42eventextractor import ExtractionHandlers
import py42.sdk

code42_sdk = py42.sdk.from_local_account(
    "https://example.authority.com",
    "admin@example.com",
    "password",
)

handlers = ExtractionHandlers()

# Add implementations for customizing handling response and getting/setting insertion timestamp cursors:
def handle_response(response):
    pass

def record_cursor_position(cursor):
    pass

def get_cursor_position():
    pass

handlers.handle_response = handle_response
handlers.record_cursor_position = record_cursor_position
handlers.get_cursor_position = get_cursor_position

extractor = FileEventExtractor(code42_sdk, handlers)
extractor.extract()

# To get all security events in a particular time range, provide an EventTimestamp filter.
# Note that if you use `record_cursor_position`, your event timestamp filter may not apply.

from py42.sdk.queries.fileevents.filters import EventTimestamp
time_filter = EventTimestamp.in_range(1564694804, 1564699999)
extractor.extract(time_filter)

```

## Usage - Code42 Security Alerts

Getting alerts is similar to getting security events, use the AlertExtractor with appropriate alert filters from the
`py42.sdk.queries.alerts.filters` module:

```python
from c42eventextractor.extractors import AlertExtractor
from py42.sdk.queries.alerts.filters import AlertState

# set up your sdk and handlers here

extractor = AlertExtractor(code42_sdk, handlers)

open_filter = AlertState.eq(AlertState.OPEN)
extractor.extract(open_filter)
```

### Handlers

A basic set of handlers is provided in the `c42eventextractor.extraction_handlers.ExtractionHandlers` class.

These default to printing the response data and any errors to the console and stores cursor position in memory.

`c42eventextractor` also provides some common logging and formatting implementations that you may find useful for
reporting on security data.

For example, to extract and submit file events to a syslog server in CEF format, use the below as your
`handle_response` implementation:

```python
import json
import logging
from c42eventextractor.logging.handlers import NoPrioritySysLogHandler
from c42eventextractor.logging.formatters import FileEventDictToCEFFormatter

my_logger = logging.getLogger("MY_LOGGER")
handler = NoPrioritySysLogHandler("examplehostname.com")
handler.setFormatter(FileEventDictToCEFFormatter())
my_logger.addHandler(handler)
my_logger.setLevel(logging.INFO)

def handle_response(response):
    events = json.loads(response.text)["fileEvents"]
    for event in events:
        my_logger.info(event)
```

To customize processing of results/errors further, or to persist cursor data to a location of your choosing, override
the methods on the provided handlers or create your own handler class with the same method signature as
`c42eventextractor.extraction_handlers.ExtractionHandlers`.

### Cursor Behavior

Because extractors automatically check for cursor checkpoints from the provided handlers, if the `.extract()` method
is called with the same filter classes used to store the checkpoint position (`DateObserved` for alerts and
`InsertionTimestamp` for file events), an exception will be raised if a cursor checkpoint already exists, as the
extractor will automatically add its own timestamp filter to the query.
