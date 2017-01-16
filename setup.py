from setuptools import setup

setup(
    name="django-asyncio-redis",
    author="Jared Mackey",
    packages=[
        'django-asyncio-redis'
    ],
    install_requirements=[
        'django>=1.8',
        'asyncio-redis'
    ]
)