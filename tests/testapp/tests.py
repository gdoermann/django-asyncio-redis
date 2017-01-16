import asynctest

from django.core.cache import cache
from django.test import SimpleTestCase

__all__ = ["TestBasicConnection"]


class TestBasicConnection(SimpleTestCase, asynctest.TestCase):
    def tearDown(self):
        cache.close()

    async def set(self, key="test-key", value="test-value"):
        resp = await cache.set(key, value)
        self.assertTrue(resp)
        return resp

    async def get(self, key="test-key"):
        return await cache.get(key)

    async def test_can_set(self):
        await self.set()
        val = await self.get()
        self.assertEqual(val, 'test-value')

    async def test_can_delete(self):
        await self.set()
        val = await self.get()
        self.assertEqual(val, 'test-value')
        await cache.delete('test-key')
        val = await self.get()
        self.assertIsNone(val)
