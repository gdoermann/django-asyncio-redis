from setuptools import setup
from django_asyncio_redis import __version__

setup(
    name="django-asyncio-redis",
    author="Jared Mackey",
    author_email='jared@mackey.tech',
    version=__version__,
    description="A asyncio-redis backend for Django!",
    url='https://github.com/mackeyja92/django-asyncio-redis',
    license='MIT License',
    packages=[
        'django_asyncio_redis'
    ],
    install_requirements=[
        'django>=1.8',
        'asyncio-redis'
    ]
)