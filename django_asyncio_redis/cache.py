from asyncio_redis.connection import Connection
from asyncio_redis.pool import Pool
from django.core.cache.backends.base import BaseCache, DEFAULT_TIMEOUT
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

ALLOWED_PROTOS = [
    "asyncio_redis.RedisProtocol",
    "asyncio_redis.HiRedisProtocol",
]


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
        self._params.pop('TIMEOUT')
        proto = self._params.pop('PROTOCOL_CLASS', ALLOWED_PROTOS[0])
        if proto not in ALLOWED_PROTOS:
            raise ImproperlyConfigured(
                "Unknown protocol class. Please chose from the following {}".format(' OR '.join(ALLOWED_PROTOS))
            )
        self.protocol_class = import_string(proto)

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
                "host": self._host,
                "port": self._port,
                "db": self._db,
                "protocol_class": self.protocol_class,
                **{k.lower(): v for k, v in self._params.items()}
            }
            if 'poolsize' not in connection_kwargs:
                self._client = await Connection.create(**connection_kwargs)
            else:
                self._client = await Pool.create(**connection_kwargs)
        return self._client

    async def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None, **kwargs):
        key = self.make_key(key, version=version)
        expire = int(self.get_backend_timeout(timeout))
        resp = await (await self.client).set(key, value, expire=expire, **kwargs)
        return resp.status == "OK"

    async def set_many(self, data, timeout=DEFAULT_TIMEOUT, version=None, **kwargs):
        expire = self.get_backend_timeout(timeout)
        for key, value in data.items():
            key = self.make_key(key, version=version)
            await (await self.client).set(key, value, expire=expire, **kwargs)

    async def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        return await self.set(key, value, timeout=timeout, version=version)

    async def get(self, key, default=None, version=None):
        key = self.make_key(key, version=version)
        result = await (await self.client).get(key)
        if not result:
            return default
        return result

    async def get_many(self, keys, version=None):
        return await (await self.client).mget_aslist((self.make_key(key, version=version) for key in keys))

    async def get_or_set(self, key, default=None, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_key(key, version=version)
        return await (await self.client).getset(key, default)

    async def has_key(self, key, version=None):
        return bool(await (await self.client).keys_aslist(self.make_key(key, version=version)))

    async def incr(self, key, delta=1, version=None):
        key = self.make_key(key, version=version)
        return await (await self.client).incrby(key, delta)

    async def decr(self, key, delta=1, version=None):
        key = self.make_key(key, version=version)
        return await (await self.client).decrby(key, delta)

    async def delete(self, key, version=None):
        key = self.make_key(key, version=version)
        await (await self.client).delete([key])

    async def delete_many(self, keys, version=None):
        await (await self.client).delete((self.make_key(key, version=version) for key in keys))

    async def clear(self):
        """
        Clears all keys. Not using flushall and instead returning a count for compatibility with other Django backends.
        """
        keys = await (await self.client).keys_aslist('*')
        count = len(keys)
        await (await self.client).delete(keys)
        return count

    def close(self, **kwargs):
        self.client.close()
        self._client = None
