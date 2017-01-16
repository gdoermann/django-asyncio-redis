import os

DATABASES = {}
SECRET_KEY = 'testing-secret-key'
TIME_ZONE = "America/Denver"
LANGUAGE_CODE = "en-us"
STATICFILES_DIRS = ()
MIDDLEWARE_CLASSES = []

REDIS_LOCATION = [os.environ.get('REDIS_LOCATION', "redis://127.0.0.1:6379?db=1")]

CACHES = {
    "default": {
        "BACKEND": "django-asyncio-redis.cache.AsyncRedisCache",
        "LOCATION": REDIS_LOCATION,
        "POOLSIZE": 5,
        "TIMEOUT": 1200,
    }
}

INSTALLED_APPS = [
    "testapp",
]

TEST_RUNNER = "runner.DatabaselessTestRunner"