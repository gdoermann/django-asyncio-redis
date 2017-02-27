from setuptools import setup

from django_asyncio_redis import __version__


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="django-asyncio-redis",
    author="Jared Mackey",
    author_email='jared@mackey.tech',
    version=__version__,
    description="A asyncio-redis backend for Django!",
    long_description=readme(),
    keywords='django asyncio redis cache',
    url='https://github.com/mackeyja92/django-asyncio-redis',
    license='MIT License',
    packages=[
        'django_asyncio_redis'
    ],
    install_requires=['django>=1.8', 'aioredis']
)
