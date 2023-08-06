# ats_sdk
SDK for alternate text service

<!-- Use markdown-toc to build the following section -->

<!-- toc -->

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Running Tests](#running-tests)
- [Releasing](#releasing)

<!-- tocstop -->

## Installation

`pip install ats_sdk`

## Basic Usage


```python
from ats_sdk import AlternateTextService

ats = AlternateTextService(
    url=Config.ATS_URL,
    cache_size=Config.MAX_CACHE_SIZE, # Optional, Default = 1024
    cache_expiry=Config.CACHE_EXPIRY  # Optional, Default = 3600 in secs
)


translated_resource = ats.translate_and_serialize(
    resource={"key": "value"},
    locale="en"
)
```

## Running Tests

- pip install ".[test]"
- pytest

## Releasing

- `make bump_patch_version`
- Update [the Changelog](https://github.com/Shuttl-Tech/ats_sdk/blob/master/Changelog.md)
- Commit changes to `Changelog`, `setup.py` and `setup.cfg`.
- `make release` (this'll push a tag that will trigger a Drone build)
