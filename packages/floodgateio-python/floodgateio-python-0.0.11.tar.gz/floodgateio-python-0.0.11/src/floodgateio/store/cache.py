
from typing import Dict, Any


class Cache:

    __store = None  # type: Dict[str, Any]

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Cache, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__store = {}

    def save(self, name, jsonData):
        # type: (str, Any) -> None
        self.__store[name] = jsonData

    def retreive(self, name):
        # type: (str) -> Any
        return self.__store.get(name)
