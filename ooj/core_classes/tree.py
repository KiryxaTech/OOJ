# (c) KiryxaTech, 2024. Apache License 2.0. See the LICENSE file.

from typing import Dict, List, Union
from ooj.core_classes import Entity, Entry


class RootTree(Entity):
    """
    Represents a hierarchical structure of Entries and Trees in the OOJ library.

    The `RootTree` class allows the creation of nested JSON-compatible entities,
    which can include both individual entries and other tree structures, forming 
    a tree-like hierarchy. Each `RootTree` instance can contain multiple `Entry` 
    or `Tree` objects, stored in a list.

    Attributes:
        tree (List[Union[Entry, RootTree]]): A list of entries and nested trees.

    Methods:
        add(entry: Union[Entry, 'RootTree']):
            Adds a new entry or subtree to the root tree.

        remove(key: str):
            Removes an entry from the tree based on its key.

        to_dict() -> Dict:
            Converts the root tree and its nested entries into a dictionary format.
    """

    def __init__(self, *entries: Union[Entry, 'RootTree']) -> None:
        """
        Initializes a RootTree instance with a list of entries or nested trees.

        Args:
            entries (Union[Entry, RootTree]): The entries or nested trees to include 
                                              in the root tree.
        """
        self.tree: List[Union[Entry, 'RootTree']] = list(entries)

    def __str__(self) -> str:
        """
        Returns a string representation of the root tree based on its dictionary form.

        Returns:
            str: A string that represents the dictionary form of the root tree.
        """
        return str(self.to_dict())

    def add(self, entry: Union[Entry, 'RootTree']):
        """
        Adds a new entry or nested tree to the root tree.

        Args:
            entry (Union[Entry, RootTree]): The entry or subtree to add.
        """
        self.tree.append(entry)

    def remove(self, key: str):
        """
        Removes an entry from the root tree based on its key.

        Args:
            key (str): The key of the entry to remove.
        """
        self.tree = [entry for entry in self.tree if not (isinstance(entry, Entry) and entry.key == key)]

    def to_dict(self) -> Dict:
        """
        Converts the root tree and its nested entries into a dictionary.

        Returns:
            Dict: A dictionary representing the root tree, with entries and subtrees.
        """
        dictionary = {}

        for entry in self.tree:
            if isinstance(entry, Entry):
                dictionary.update(entry.to_dict())
            elif isinstance(entry, RootTree):
                dictionary[entry.key] = entry.to_dict()

        return dictionary


class Tree(RootTree):
    """
    Represents a tree with a key that can be part of a RootTree or other Trees.

    The `Tree` class is a specialized version of `RootTree` that includes a unique key.
    It can contain other entries or trees, allowing for the creation of deeply nested
    tree structures within a `RootTree`.

    Attributes:
        key (str): The unique key identifying the tree.

    Methods:
        Inherits all methods from `RootTree`.
    """

    def __init__(self, key: str, *entries: Union[Entry, 'Tree']) -> None:
        """
        Initializes a Tree instance with a unique key and list of entries or subtrees.

        Args:
            key (str): The unique key of the tree.
            entries (Union[Entry, Tree]): The entries or nested trees to include.
        """
        super().__init__(*entries)
        self.key = key


class TreeConverter:
    """
    Utility class for converting between JSON data and OOJ tree structures.

    The `TreeConverter` class provides methods for converting JSON-like dictionaries 
    into `RootTree` or `Tree` objects and vice versa. This allows for seamless 
    transitions between JSON and OOJ structures.

    Methods:
        to_root_tree(json_data: dict) -> RootTree:
            Converts a dictionary to a `RootTree` object.

        to_tree(key: str, json_data: dict) -> Tree:
            Converts a dictionary with a specified key to a `Tree` object.

        to_dict(json_object: Union[Entry, Tree, RootTree]) -> Dict:
            Converts an OOJ object (Entry, Tree, or RootTree) back into a dictionary.
    """

    @classmethod
    def to_root_tree(cls, json_data: dict) -> RootTree:
        """
        Converts a dictionary to a `RootTree` object.

        Args:
            json_data (dict): The dictionary to convert.

        Returns:
            RootTree: A `RootTree` representing the dictionary structure.
        """
        root_tree = RootTree()
        
        for key, value in json_data.items():
            if isinstance(value, dict):
                subtree = cls.to_tree(key, value)
                root_tree.add(subtree)
            else:
                root_tree.add(Entry(key, value))

        return root_tree

    @classmethod
    def to_tree(cls, key: str, json_data: dict) -> Tree:
        """
        Converts a dictionary with a specified key to a `Tree` object.

        Args:
            key (str): The key identifying the tree.
            json_data (dict): The dictionary to convert.

        Returns:
            Tree: A `Tree` representing the dictionary structure.
        """
        tree = Tree(key)
        
        for entry_key, entry_value in json_data.items():
            if isinstance(entry_value, dict):
                subtree = cls.to_tree(entry_key, entry_value)
                tree.add(subtree)
            else:
                tree.add(Entry(entry_key, entry_value))
        
        return tree
    
    @classmethod
    def to_dict(cls, json_object: Union[Entry, Tree, RootTree]) -> Dict:
        """
        Converts an OOJ object (Entry, Tree, or RootTree) back into a dictionary.

        Args:
            json_object (Union[Entry, Tree, RootTree]): The OOJ object to convert.

        Returns:
            Dict: A dictionary representation of the OOJ object.
        """
        return dict(json_object)