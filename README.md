# django-asyncio-redis
A `asyncio-redis` backend for Django

This project is currently in alpha. Basic functionality is working but I am testing out various ideas for loop 
management and haven't fully tested all the endpoints yet. Currently, the implementation will setup a connection 
on first use with whatever loop the `asyncio-redis` library pulls (`asyncio.get_event_loop()`). This is not exactly an ideal 
situation but I haven't been able to figure out how to manage loops in a global state object like `django.core.cache.cache`. 
