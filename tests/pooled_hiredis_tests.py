import os

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
        "PROTOCOL_CLASS": "asyncio_redis.HiRedisProtocol",
        "LOCATION": REDIS_LOCATION,
    }
}

INSTALLED_APPS = [
    "testapp",
]

TEST_RUNNER = "runner.DatabaselessTestRunner"
