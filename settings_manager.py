import json
from typing import List, Union, Tuple
class SettingsNotLocked(Exception):
    pass

class Settings:
    def __init__(self, js: dict) -> None:
        self._js = js
        print(self._js)
    
    def add(self, name: str, id_: str, location: str) -> None:
        self._js["names"][id_] = name
        self._js["locs"][id_] = location

    def get_names(self) -> Union[List[Tuple[str, str]], None]:
        try:
            return self._js["names"].values()
        except (IndexError, KeyError):
            return None

    def get_location(self, id_: str) -> Union[str, None]:
        try:
            return self._js["locs"][id_]
        except (IndexError, KeyError):
            return None

    def get(self) -> dict:
        ret = self._js 
        del self
        return ret


class SettingsManager:
    def __init__(self) -> None:
        self.filename = "settings.json"
        self.lock = None
    
    def __enter__(self) -> Settings:
        while self.lock is not None:
            pass
        self.lock = Settings(json.load(open(self.filename))["settings"])
        return self.lock
    
    def __exit__(self, *_args) -> None:
        json.dump({"settings": self.lock.get()}, open(self.filename, "w"))
        self.lock = None