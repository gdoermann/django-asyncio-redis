# django-asyncio-redis
A `aioredis` backend for Django.

This project is currently in alpha. Basic functionality is working but I am testing out various ideas for loop 
management and haven't fully tested all the endpoints yet. Currently, the implementation will setup a connection 
on first use with whatever loop the `aioredis` library pulls (`asyncio.get_event_loop()`). This is not exactly an ideal 
situation but I haven't been able to figure out how to manage loops in a global state object like `django.core.cache.cache`. 

### Usage
`pip install django-asyncio-redis`

The following will set your cache backend to the `AsyncRedisCache`. It will be using `HiRedis` and connection pooling. 
HiRedis is the preferred backend as it is very fast.  


```python
# settings.py
import os

CACHES = {
    "default": {}, # Leave your default the way it was for non async django access.
    "async": {
        "BACKEND": "django-asyncio-redis.cache.AsyncRedisCache",
        "LOCATION": os.environ.get('REDIS_LOCATION', "redis://127.0.0.1:6379?db=1"),
        "POOLSIZE": 5,
        "TIMEOUT": 1200,
    }
}

```
```python
# views.py
from django.core.cache import caches
from django.http import HttpResponse
acache = caches['async']
async def my_view(request):
    val = await acache.get('test-key')
    return HttpResponse(val)
```

### All fields:
* `LOCATION`
   * Required. 
   * Specified as `redis://host:port` with optional `?db=x` to specify the database.
* `POOLSIZE`
  * Optional. Default: 10.
* `LOOP`
    * Optional. Default `None`.
    * The IO loop to run everything on.
* `TIMEOUT`
  * Optional. Default 300.
  * Specify the default cache expire time. Used in `set` type operations.
* `ENCODER`
    * Optional. Default `django_asyncio_redis.encoder.JSONEncoder`
    * Determines how the data is encoded to be transmitted to redis.
