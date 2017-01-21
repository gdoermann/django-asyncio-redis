import asynctest

from django.core.cache import cache
from django.test import SimpleTestCase

__all__ = ["TestBasicConnection"]


class TestBasicConnection(SimpleTestCase, asynctest.TestCase):
    def tearDown(self):
        cache.close()

    async def set(self, value, key="test-key"):
        resp = await cache.set(key, value)
        self.assertTrue(resp)
        return resp

    async def get(self, key="test-key"):
        return await cache.get(key)

    async def test_can_set(self):
        v = 'test-value'
        await self.set(v)
        val = await self.get()
        self.assertEqual(val, 'test-value')

    async def test_can_delete(self):
        v = 'test-value'
        await self.set(v)
        val = await self.get()
        self.assertEqual(val, v)
        await cache.delete('test-key')
        val = await self.get()
        self.assertIsNone(val)

    async def test_with_various_data_types(self):
        await self.set(u'value')
        val = await self.get()
        self.assertEqual(val, u'value')

        await self.set([1, 2, 3])
        val = await self.get()
        self.assertEqual(val, [1, 2, 3])

        await self.set({'k': 'v'})
        val = await self.get()
        self.assertEqual(val, {'k': 'v'})

        await self.set(1)
        val = await self.get()
        self.assertEqual(val, 1)

    async def test_with_complex_nested_types(self):
        v = [
            {'k': 1, 'k2': 'v', 'k3': {"k": "v"}},
            [1,2,3],
            "val",
            1
        ]
        await self.set(v)
        val = await self.get()
        self.assertEqual(val, v)