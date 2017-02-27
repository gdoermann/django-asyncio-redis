import os

import asyncio

DATABASES = {}
SECRET_KEY = 'testing-secret-key'
TIME_ZONE = "America/Denver"
LANGUAGE_CODE = "en-us"
STATICFILES_DIRS = ()
MIDDLEWARE_CLASSES = []

REDIS_LOCATION = os.environ.get('REDIS_LOCATION', "redis://127.0.0.1:6379?db=1")

CACHES = {
    "default": {
        "BACKEND": "django_asyncio_redis.cache.AsyncRedisCache",
        "POOLSIZE": 5,
        "LOCATION": REDIS_LOCATION,
        "LOOP": asyncio.get_event_loop()
    }
}

INSTALLED_APPS = [
    "testapp",
]

TEST_RUNNER = "runner.DatabaselessTestRunner"
