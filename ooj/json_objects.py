from typing import Any, Dict, List, Union
from abc import ABC, abstractmethod


class JsonObject(ABC):
    def __str__(self):
        return str(self.to_dict())
    
    @abstractmethod
    def to_dict(self) -> Dict:
        pass


class Entry(JsonObject):
    """
    Представляет пару ключ-значение.
    """
    def __init__(self, key: str, value: Any) -> None:
        self.key = key
        self.value = value

    def __str__(self):
        return str(self.to_dict())
    
    def to_dict(self):
        return {self.key: self.value}


class BaseTree(JsonObject):
    def __init__(self, *entries: Union[Entry, 'BaseTree']) -> None:
        self.tree: List[Union[Entry, 'BaseTree']] = list(entries)

    def __str__(self) -> str:
        return str(self.to_dict())

    def add(self, entry: Union[Entry, 'BaseTree']):
        self.tree.append(entry)

    def remove(self, key: str):
        self.tree = [entry for entry in self.tree if not (isinstance(entry, Entry) and entry.key == key)]

    def to_dict(self) -> Dict:
        dictionary = {}
        
        for entry in self.tree:
            if isinstance(entry, Entry):
                dictionary.update(entry.to_dict())
            elif isinstance(entry, BaseTree):
                dictionary[entry.key] = entry.to_dict()  # Используем key для поддеревьев

        return dictionary


class RootTree(BaseTree):
    def __init__(self, *entries: Union[Entry, 'BaseTree']) -> None:
        super().__init__(*entries)


class Tree(BaseTree):
    def __init__(self, key: str, *entries: Union[Entry, 'BaseTree']) -> None:
        super().__init__(*entries)
        self.key = key