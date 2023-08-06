## Anole

Like a anole, fake everything.

Currently support user agent fake, other will be coming soon.

Thanks for use.


### How to use
```python
from anole import UserAgent


# Suppose this is the request headers
headers = {
    "referer": "https://leesoar.com"
}
user_agent = UserAgent()
user_agent.fake(headers)
```

> It will check if there is "user-agent" in headers. If not, "user-agent" will update with random.

### Use as fake_useragent
```python
from anole import UserAgent


user_agent = UserAgent()
user_agent.random
# or user_agent.chrome
# or other browsers
```
