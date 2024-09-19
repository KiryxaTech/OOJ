from typing import Union, Tuple


class Entry:
    def __new__(cls, key, value):
        instance = super().__new__(cls)
        instance.key = key
        instance.value = value

        return key

    def __init__(self, key, value) -> None:
        self.key = key
        self.value = value
    

class NestedEntry:
    def __new__(cls, *nested_entries: Tuple[Union[str, Entry]], value):
        instance = super().__new__(cls)
        instance.nested_entries = nested_entries
        instance.value = value

        return nested_entries

    def __init__(self, *nested_entries, value) -> None:
        self.nested_entries = nested_entries
        self.value = value


class Tree:
    def __init__(self, *entries: Tuple[Union[Entry, NestedEntry]]):
        self.tree = list(entries)

    def add(key: Union[Entry, NestedEntry]):
        pass

    def remove(self, *keys: Union[Entry, NestedEntry]):
        pass