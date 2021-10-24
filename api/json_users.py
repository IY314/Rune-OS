import json
from dataclasses import dataclass


@dataclass
class JSONFile:
    filename: str

    def get(self):
        with open(self.filename) as f:
            return json.loads(f.read())

    def replace(self, obj):
        with open(self.filename, 'w') as f:
            f.write(json.dumps(obj, indent=4))

    def get_key(self, key):
        return self.get().get(key)

    def modify(self, key, value):
        data = self.get()
        data[key] = value
        self.replace(data)
