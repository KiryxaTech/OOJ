# (c) KiryxaTech, 2024. Apache License 2.0. See the LICENSE file.

from typing import Any
from ooj.core_classes import Entity


class Entry(Entity):
    """
    Represents a key-value pair in the OOJ library.

    The `Entry` class inherits from `Entity` and is used to create simple 
    key-value structures. Each instance stores a single key and its associated 
    value, which can be converted into a dictionary format for JSON compatibility.

    Attributes:
        key (str): The key of the entry.
        value (Any): The value associated with the key.

    Methods:
        __str__() -> str:
            Returns a string representation of the key-value pair as a dictionary.
        
        __iter__():
            Allows iteration over the key-value pair, yielding dictionary items.

        to_dict() -> Dict[str, Any]:
            Returns the key-value pair as a dictionary, in the form {key: value}.
    """

    def __init__(self, key: str, value: Any) -> None:
        """
        Initializes an Entry instance with a specified key and value.

        Args:
            key (str): The key of the entry.
            value (Any): The value associated with the key.
        """
        self.key = key
        self.value = value

    def __str__(self):
        """
        Returns a string representation of the key-value pair as a dictionary.

        Returns:
            str: A string representation of the entry in dictionary form.
        """
        return str(self.to_dict())
    
    def __iter__(self):
        """
        Allows iteration over the key-value pair as dictionary items.
        
        Yields:
            Tuple[str, Any]: Key-value pairs from the dictionary representation.
        """
        return iter(self.to_dict().items())
    
    def to_dict(self):
        """
        Returns the key-value pair as a dictionary.

        Returns:
            Dict[str, Any]: A dictionary in the form {key: value}.
        """
        return {self.key: self.value}