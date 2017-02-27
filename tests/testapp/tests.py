import asynctest

from django.test import SimpleTestCase
from django.core.cache import cache
from django.conf import settings

__all__ = ["TestBasicConnection"]


class TestBasicConnection(SimpleTestCase, asynctest.TestCase):
    use_default_loop = True

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

    async def test_set_get_many(self):
        data = {
            'key1': 'value1',
            'key2': 'value2'
        }
        await cache.set_many(data)
        results = await cache.get_many(data.keys())
        self.assertDictEqual(results, data)
        data['non_existing'] = None
        results = await cache.get_many(data.keys())
        self.assertDictEqual(results, data)

    async def test_can_delete(self):
        v = 'test-value'
        await self.set(v)
        val = await self.get()
        self.assertEqual(val, v)
        self.assertEqual(1, await cache.delete('test-key'))
        val = await self.get()
        self.assertIsNone(val)

    async def test_delete_many(self):
        await self.set('test', 'test-1')
        await self.set('test2', 'test-2')
        await cache.delete_many(('test-1', 'test-2'))
        self.assertIsNone(await self.get('test-1'))
        self.assertIsNone(await self.get('test-2'))

    async def test_clear(self):
        # pre-clear
        await cache.clear()

        await self.set('test')
        await self.set('test2', key='test-2')
        self.assertEqual(2, await cache.clear())
        self.assertIsNone(await self.get())
        self.assertIsNone(await self.get('test-2'))

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

    async def test_check_loop(self):
        self.assertEqual(id(cache.loop), id(settings.CACHES['default'].get('LOOP')))

    async def test_incr(self):
        key = 'key-to-incr'
        await cache.set(key, 1)
        await cache.incr(key)
        result = await cache.get(key)
        self.assertEqual(result, 2)

    async def test_decr(self):
        key = 'key-to-decr'
        await cache.set(key, 10)
        await cache.decr(key)
        result = await cache.get(key)
        self.assertEqual(result, 9)
