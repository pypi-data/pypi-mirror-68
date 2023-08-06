[![PyPI version](https://badge.fury.io/py/nonfig-sdk.svg)](https://badge.fury.io/py/nonfig-sdk)
[![CircleCI](https://circleci.com/gh/nonfig/python-sdk/tree/master.svg?style=shield)](https://circleci.com/gh/nonfig/python-sdk/tree/master)


# Python SDK

The open source SDK will ease the integration with your platform if you are running on Python. For more information about the documentation, please check out [docs.nonfig.com](https://docs.nonfig.com)

The package is already published (https://pypi.org/project/nonfig-sdk/)[https://pypi.org/project/nonfig-sdk/]

### Example code

```python
from nonfig.sdk import Nonfig

options = {
    'app_id': "c1e8293f-58be-4c55-9db4-b1c39cbc1dcb",  # Replace with your App ID
    'app_secret': "XuuhXorEZqeRTJjHumGCgnPuZMdQgVvu",  # Replace with your App Secret
    'debug': True,
    'cache_enable': True,
    'cache_ttl': 60
}
nonfig = Nonfig(options)
```

## Docs

We have extensive documentation available [here](https://docs.nonfig.com/sdk/python) at the disposal. You shall be able to find example or sample codes too.

## Guidelines

Please apply a correct label whether you are filing a Bug, Suggestion or just a question.

- Bug = `bug`
- Suggestion = `feature`
- Question = `help`


## Contribution

The project is maintained by the Nonfig's Core Team and following contributors (if any).
