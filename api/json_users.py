import json
from typing import Any, Dict


class JSONFile(object):

    def __init__(self, filename: str) -> None:
        self.filename: str = filename
    
    def get(self) -> Dict[str, Any]:
        with open(self.filename) as f:
            return json.loads(f.read())
    
    def replace(self, obj: Dict[str, Any]) -> None:
        with open(self.filename, 'w') as f:
            f.write(json.dumps(obj, indent=4))
    
    def get_key(self, key: str) -> Any:
        return self.get().get(key)
    
    def modify(self, key: str, value: Any) -> None:
        data = self.get()
        data[key] = value
        self.replace(data)
