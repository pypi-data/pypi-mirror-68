# curious-slido

Sends your questions to a [sli.do](https://sli.do) event

## How to install

```
pip install curious-slido 
```

## How to use

```python
from curious_slido import SlidoClient

# You can grab it from URL with event, for example
# https://app.sli.do/event/abcd1234/live/questions -> event_hash = 'abcd1234'
event_hash = 'abcd1234'

# You can grab it from cookie Slido.EventAuthTokens (part after comma) or from 
# any api request: 
# Developer Tools -> Network -> (request to api.sli.do) -> Headers -> Request headers -> authorization (part after `Bearer`)
auth_token = 'longlonglongstring'

slido_client = SlidoClient(event_hash=event_hash, auth_token=auth_token)
slido_client.send_question('Your question')
```