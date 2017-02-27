import json

from django.utils.encoding import force_bytes, force_text


class JSONEncoder:
    def encode(self, data):
        return force_bytes(json.dumps(data))

    def decode(self, data):
        return json.loads(force_text(data))