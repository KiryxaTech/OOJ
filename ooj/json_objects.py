from typing import Any, Dict, List, Union


class Entry:
    """
    Представляет пару ключ-значение.
    """
    def __init__(self, key: str, value: Any) -> None:
        self.key = key
        self.value = value


class BaseTree:
    """
    Базовый класс для дерева. Определяет общие методы для работы с узлами дерева.
    """
    def __init__(self, *entries: Union[Entry, 'BaseTree']) -> None:
        self.tree: List[Union[Entry, 'BaseTree']] = list(entries)

    def add(self, entry: Union[Entry, 'BaseTree']):
        """
        Добавляет элемент (Entry или поддерево) в текущее дерево.
        """
        self.tree.append(entry)

    def remove(self, key: str):
        """
        Удаляет элемент из дерева по ключу.
        """
        self.tree = [entry for entry in self.tree if not (isinstance(entry, Entry) and entry.key == key)]

    def to_dict(self) -> Dict:
        """
        Преобразует дерево и поддеревья в словарь.
        """
        dictionary = {}

        for entry in self.tree:
            if isinstance(entry, Entry):
                dictionary[entry.key] = entry.value
            elif isinstance(entry, BaseTree) and hasattr(entry, 'key'):
                dictionary[entry.key] = entry.to_dict()

        return dictionary


class RootTree(BaseTree):
    def __init__(self, *entries: Union[Entry, 'BaseTree']) -> None:
        super().__init__(*entries)


class Tree(BaseTree):
    def __init__(self, key: str, *entries: Union[Entry, 'BaseTree']) -> None:
        super().__init__(*entries)
        self.key = key