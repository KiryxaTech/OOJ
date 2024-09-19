from typing import Union, Tuple


class Entry:
    def __new__(cls, name, value):
        instance = super().__new__(cls)
        instance.__name = name
        instance.value = value

        return name

    def __init__(self, name, value) -> None:
        self.__name = name
        self.value = value
    

class NestedEntry:
    def __new__(cls, *inner_names, value):
        instance = super().__new__(cls)
        instance.__inner_names = inner_names
        instance.value = value

        return inner_names

    def __init__(self, *inner_names, value) -> None:
        self.__inner_names = inner_names
        self.value = value


class Tree:
    def __init__(self, *keys: Tuple[Union[Entry, NestedEntry]]):
        self.__tree = list(keys)

    def add(key: Union[Entry, NestedEntry]):
        pass

    def remove(self, *keys: Union[Entry, NestedEntry]):
        pass