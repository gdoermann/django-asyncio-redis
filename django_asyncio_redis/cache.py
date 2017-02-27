import asyncio
from aioredis import create_pool
from django.core.cache.backends.base import BaseCache, DEFAULT_TIMEOUT
from django.utils.module_loading import import_string

default_encoder = 'django_asyncio_redis.encoder.JSONEncoder'


class AsyncRedisCache(BaseCache):
    def __init__(self, server, params):
        super().__init__(params)
        self._client = None

        self._server = server
        self._host = None
        self._port = 6379
        self._db = 0
        self._parse_server()
        self._params = params
        self._params.pop('TIMEOUT', None)

        self.loop = params.pop('LOOP', None)
        if not self.loop:
            self.loop = asyncio.get_event_loop()

        self.pool_size = self._params.pop('POOLSIZE', 10)

        encoder = self._params.pop('ENCODER', default_encoder)
        self.encoder_class = import_string(encoder)
        self.encoder = self.encoder_class()

    def _parse_server(self):
        host_and_port = self._server.split("redis://")[1]
        host, port = host_and_port.split(":")
        if '?' in port:
            port, db = port.split("?")
            if db:
                self._db = int(db[-1])
        self._host = host
        if port:
            self._port = int(port)

    def get_backend_timeout(self, timeout=DEFAULT_TIMEOUT):
        if timeout == DEFAULT_TIMEOUT:
            timeout = int(self.default_timeout)
        elif timeout == 0:
            timeout = None
        return timeout

    @property
    async def client(self):
        """
        Lazily setup client connection
        """
        if self._client is None:
            connection_kwargs = {
                "db": self._db,
                "maxsize": self.pool_size,
                "loop": self.loop,
                **{k.lower(): v for k, v in self._params.items()}
            }
            self._client = await create_pool(
                (self._host, self._port),
                **connection_kwargs
            )
        return self._client

    async def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None, **kwargs):
        key = self.make_key(key, version=version)
        expire = self.get_backend_timeout(timeout)
        with await (await self.client) as client:
            return await client.set(key, self.encoder.encode(value), expire=expire, **kwargs)

    async def set_many(self, data, timeout=DEFAULT_TIMEOUT, version=None, **kwargs):
        expire = self.get_backend_timeout(timeout)
        with await (await self.client) as client:
            for key, value in data.items():
                key = self.make_key(key, version=version)
                await client.set(key, self.encoder.encode(value), expire=expire, **kwargs)

    async def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        return await self.set(key, value, timeout=timeout, version=version)

    async def get(self, key, default=None, version=None):
        key = self.make_key(key, version=version)
        with await (await self.client) as client:
            result = await client.get(key)
            if not result:
                return default
            return self.encoder.decode(result)

    async def get_many(self, keys, version=None):
        versioned_keys = [self.make_key(key, version=version) for key in keys]
        with await (await self.client) as client:
            cache_results = await client.mget(*versioned_keys)
            final_results = {}
            for key, result in zip(keys, cache_results):
                if isinstance(result, bytes):
                    final_results[key] = self.encoder.decode(result)
                else:
                    final_results[key] = result
            return final_results

    async def get_or_set(self, key, default=None, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_key(key, version=version)
        with await (await self.client) as client:
            results = await client.getset(key, self.encoder.encode(default))
            return self.encoder.decode(results)

    async def has_key(self, key, version=None):
        with await (await self.client) as client:
            return bool(await client.exists(self.make_key(key, version=version)))

    async def incr(self, key, delta=1, version=None):
        key = self.make_key(key, version=version)
        with await (await self.client) as client:
            return await client.incrby(key, delta)

    async def decr(self, key, delta=1, version=None):
        key = self.make_key(key, version=version)
        with await (await self.client) as client:
            return await client.decrby(key, delta)

    async def delete(self, key, version=None):
        key = self.make_key(key, version=version)
        with await (await self.client) as client:
            return await client.delete(key)

    async def delete_many(self, keys, version=None):
        with await (await self.client) as client:
            return await client.delete(*(self.make_key(key, version=version) for key in keys))

    async def clear(self):
        """
        Clears all keys. Not using flushall and instead returning a count for compatibility with other Django backends.
        """
        with await (await self.client) as client:
            keys = await client.keys(self.make_key('*'))
            count = len(keys)
            await client.delete(*keys)
            return count

    # Django closes the cache after every request. We don't need to do that.
    # async def close(self, **kwargs):
    #     if self._client:
    #         self._client.close()
    #         await self._client.wait_closed()
    #         self._client = None
