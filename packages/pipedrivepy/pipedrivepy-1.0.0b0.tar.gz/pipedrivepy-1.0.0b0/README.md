# pipedrivepy
*Pipedrive API generic client for Python*

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linter: pylint](https://img.shields.io/badge/linter-pylint-blue.svg)](https://github.com/PyCQA/pylint)


## Requirements
pipedrivepy tested under Python 3.6+. Synchoronous version requires `requests` package. Asynchoronous version requires `aiohttp` package.


## Installation

You can install pipedrivepy with:

- `pip install pipedrivepy[sync]` for synchoronous version;
- `pip install pipedrivepy[async]` for asynchoronous version;


# Usage
[Pipedrive API Reference](https://developers.pipedrive.com/docs/api/v1/)

pipedrivepy uses chain technique to build endpoint path.

For example, `client.deals(100).followers` makes path to `/deals/100/followers`.

To send request need call one of control methods:

- `get(**query)` to GET request;
- `add(**payload)` to POST request;
- `update(**payload)` to PUT request;
- `delete(**payload)` to DELETE request;

You must first check API method signature to build right path and call right method.

### Example usage of synchoronous client
```python
"""Add a deal
https://developers.pipedrive.com/docs/api/v1/#!/Deals/post_deals"""

from pipedrive import PipedriveError
from pipedrive.sio import Client

client = Client('your-company-domain', 'your-token')

def add_deal(title):
    try:
        data = client.deals.add(title='Test deal')
    except PipedriveError as error:
        print(error.code)  # Show HTTP code
        raise ValueError(str(error))

    print(data['data']['id'])
```

### Example usage of asynchoronous client
```python
"""Merging two deals
https://developers.pipedrive.com/docs/api/v1/#!/Deals/put_deals_id_merge"""

from pipedrive import PipedriveError
from pipedrive.aio import Client

client = Client('your-company-domain', 'your-token')

async def merge_deals(deal_id, merge_with_id):
    try:
        data = await client.deals(42).merge.update(merge_with_id=24)
    except PipedriveError as error:
        print(error.code)  # Show HTTP code
        raise ValueError(str(error))

    print(data['data']['id'])
```


# License
[MIT](https://github.com/bindlock/pipedrivepy/blob/master/LICENSE)
