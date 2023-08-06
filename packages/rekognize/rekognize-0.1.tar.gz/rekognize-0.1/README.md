# Rekognize Twitter API Client

Rekognize Python Twitter REST API client for accessing Twitter data


## Installation

The easiest and recommended way to install `rekognize` is from [PyPI](https://pypi.python.org/pypi/rekognize)

```
pip install rekognize
```

## Usage

> Before you get started, you will need to [authorize](https://rekognize.io/login) Rekognize Twitter application to obtain your `ACCESS_TOKEN` and `ACCESS_TOKEN_SECRET`. It's free.


Import client and initialize it:

```python
from rekognize.twitter import UserClient

ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
ACCESS_TOKEN_SECRET = 'YOUR_ACCESS_TOKEN_SECRET'

client = UserClient(
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)
```

## Examples

```python
# users/show
response = client.api.users.show.get(screen_name='twitter')
response.data
```


Actually any call can be written in this alternative syntax, use whichever you prefer. Both syntax forms can be freely combined as in the example above. Some more examples:

```python
response = client.api['users/show'].get(screen_name='twitter')

response = client.api['users']['show'].get(screen_name='twitter')

response = client.api['statuses/destroy']['240854986559455234'].post()
```

Response is a dictionary that contains the data returned and the remaining API calls you can make. Remaining count is reset in 15 minutes. 


## Exceptions

There are 4 types of exceptions in `birdy` all subclasses of base `BirdyException` (which is never directly raised).

  - `TwitterClientError` raised for connection and access token retrieval errors
  - `TwitterApiError` raised when Twitter returns an error
  - `TwitterAuthError` raised when authentication fails,
    `TwitterApiError` subclass
  - `TwitterRateLimitError` raised when rate limit for resource is reached, `TwitterApiError` subclass

