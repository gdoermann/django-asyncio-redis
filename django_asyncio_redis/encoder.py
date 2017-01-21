import json

from asyncio_redis.encoders import BaseEncoder
from django.utils.encoding import force_bytes, force_text


class JSONEncoder(BaseEncoder):
    native_type = object

    def encode_from_native(self, data):
        return force_bytes(json.dumps(data))

    def decode_to_native(self, data):
        return json.loads(force_text(data))