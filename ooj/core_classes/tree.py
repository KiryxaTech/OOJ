# (c) KiryxaTech, 2024. Apache License 2.0. See the LICENSE file.

from typing import Dict, List, Optional, Union
from ooj.core_classes import Entity, Entry


class Tree(Entity):
    """
    Represents a hierarchical structure of Entries and Trees in the OOJ library.

    The `Tree` class allows the creation of nested JSON-compatible entities,
    which can include both individual entries and other tree structures, forming 
    a tree-like hierarchy. Each `Tree` instance can contain multiple `Entry` 
    or `Tree` objects, stored in a list.

    Attributes:
        tree (List[Union[Entry, Tree]]): A list of entries and nested trees.
        _relationship_keys (Dict[str, List[str]]): A dictionary representing 
                                                  entry keys associated with 
                                                  specific relationships.
    """

    def __init__(self, *entries: Union[Entry, 'Tree'], 
                 relationships: Optional[Dict[str, List[str]]] = None) -> None:
        """
        Initializes a Tree instance with a list of entries or nested trees.

        Args:
            entries (Union[Entry, Tree]): The entries or nested trees to include 
                                          in the root tree.
            relationships (Optional[Dict[str, List[str]]]): A dictionary of relationships
                                                            using entry keys.
        """
        self.tree: List[Union[Entry, 'Tree']] = list(entries)
        self._relationship_keys = relationships if relationships is not None else {}

    def __str__(self) -> str:
        """
        Returns a string representation of the root tree based on its dictionary form.

        Returns:
            str: A string that represents the dictionary form of the root tree.
        """
        return str(self.to_dict())

    def add(self, entry: Union[Entry, 'Tree']):
        """
        Adds a new entry or nested tree to the root tree.

        Args:
            entry (Union[Entry, Tree]): The entry or subtree to add.
        """
        self.tree.append(entry)

    def remove(self, key: str):
        """
        Removes an entry from the root tree based on its key.

        Args:
            key (str): The key of the entry to remove.
        """
        self.tree = [
            entry for entry in self.tree if not (isinstance(entry, Entry) and entry.key == key)
        ]

    def to_dict(self) -> Dict:
        """
        Converts the root tree and its nested entries into a dictionary.

        Returns:
            Dict: A dictionary representing the root tree, with entries and subtrees.
        """
        dictionary = {}

        for entry in self.tree:
            if isinstance(entry, Entry):
                if isinstance(entry.value, Tree):
                    dictionary[entry.key] = entry.value.to_dict()  # Recursive subtree addition
                else:
                    dictionary[entry.key] = entry.value  # Add value from Entry
            else:
                raise TypeError("The element must be an instance of Entry.")
        
        return dictionary
    
    def get_relationship(self, name: str) -> set:
        """
        Retrieves the values of each entry key associated with a specific relationship name.

        This method returns a set of values corresponding to the entry keys in a given 
        relationship. It retrieves each entry by key and adds its value to the result set 
        if the entry is found.

        Args:
            name (str): The name of the relationship to retrieve values for.

        Returns:
            set: A set of values corresponding to each entry key in the specified relationship.
        """
        related_entries = set()
        if name in self._relationship_keys:
            for key in self._relationship_keys[name]:
                entry = self._get_entry_by_key(key)
                if entry:
                    related_entries.add(entry.value)  # Add entry's value to result set
        return related_entries

    def _get_entry_by_key(self, key: str) -> Union[Entry, None]:
        """
        Searches for and returns an Entry based on its key.

        Args:
            key (str): The key of the entry to search for.

        Returns:
            Union[Entry, None]: The found Entry object, or None if no entry matches the key.
        """
        for entry in self.tree:
            if isinstance(entry, Entry) and entry.key == key:
                return entry
        return None

    @classmethod
    def to_tree(cls, data: dict) -> 'Tree':
        """
        Converts a dictionary into a `Tree` object, creating a hierarchical structure.

        Args:
            data (dict): The dictionary to convert into a `Tree`. Keys represent 
                         the entries, and values can be either primitive types 
                         or nested dictionaries representing subtrees.

        Returns:
            Tree: A `Tree` instance representing the dictionary structure, where 
                  each key corresponds to an `Entry`, and nested dictionaries are 
                  recursively converted into subtree objects.
        """
        tree = Tree()
        
        for entry_key, entry_value in data.items():
            if isinstance(entry_value, dict):
                # Recursively convert nested dictionaries to subtrees
                subtree = cls.to_tree(entry_value)
                tree.add(Entry(entry_key, subtree))  # Use key and subtree as value
            else:
                # If the value is a primitive, create an Entry with this value
                tree.add(Entry(entry_key, entry_value))

        return tree