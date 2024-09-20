# (c) KiryxaTech, 2024. Apache License 2.0

from typing import Any, Dict, List, Union, override
from abc import ABC, abstractmethod


class JsonObject(ABC):
    def __str__(self):
        return str(self.to_dict())
    
    @abstractmethod
    def to_dict(self) -> Dict: pass


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
                dictionary[entry.key] = entry.to_dict()

        return dictionary


class RootTree(BaseTree):
    def __init__(self, *entries: Union[Entry, 'BaseTree']) -> None:
        super().__init__(*entries)


class Tree(BaseTree):
    def __init__(self, key: str, *entries: Union[Entry, 'BaseTree']) -> None:
        super().__init__(*entries)
        self.key = key


class TreeConverter:
    @classmethod
    def to_root_tree(cls, json_data: dict) -> RootTree:
        root_tree = RootTree()
        
        for key, value in json_data.items():
            if isinstance(value, dict):
                # Рекурсивно обрабатываем словари для вложенных деревьев
                subtree = cls.to_tree(key, value)
                root_tree.add(subtree)
            else:
                # Добавляем пары ключ-значение в RootTree
                root_tree.add(Entry(key, value))

        return root_tree

    @classmethod
    def to_tree(cls, key: str, json_data: dict) -> Tree:
        tree = Tree(key)
        
        for entry_key, entry_value in json_data.items():
            if isinstance(entry_value, dict):
                # Рекурсивно создаем поддерево
                subtree = cls.to_tree(entry_key, entry_value)
                tree.add(subtree)
            else:
                # Добавляем обычные записи
                tree.add(Entry(entry_key, entry_value))
        
        return tree
    
    @classmethod
    def to_dict(cls, json_object: Union[Entry, Tree, RootTree]) -> Dict:
        return json_object.to_dict()