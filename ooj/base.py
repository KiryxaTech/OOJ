# (c) KiryxaTech, 2024. Apache License 2.0. See the LICENSE file.

from abc import ABC, abstractmethod
from typing import Any, Dict, Union

from ooj.core_classes import Tree


class Readable(ABC):
    def __init__(self, fp: str):
        self._fp = fp

    @abstractmethod
    def read(self): pass


class Writable(ABC):
    def __init__(self, fp: str) -> None:
        self._fp = fp

    @abstractmethod
    def write(self, data: Union[Dict[str, Any], Tree]): pass


class JsonBase(ABC):
    """
    A base class for handling JSON data with optional file operations.

    Attributes:
        data (Dict[str, Any]): The JSON data.
    """

    def __init__(self, data: Union[Dict[str, Any], Tree]):
        """
        Initializes the JsonBaseClass instance.

        Args:
            data (Dict[str, Any]): The JSON data. Defaults to an empty dictionary.
        """
        self.__buffer: Tree = None

    def __str__(self) -> str:
        """
        Returns the JSON data as a formatted string.

        Returns:
            str: The JSON data as a string.
        """
        return str(self.__buffer)
    
    def __dict__(self) -> Dict[str, Any]:
        """
        Returns the JSON data as a formatted Dict[str, Any].

        Returns:
            Dict[str, Any]: The JSON data as a dict.
        """
        return self.__buffer.to_dict()
    
    def get_buffer_dict(self) -> dict:
        return self.__buffer.to_dict()

    def get_buffer_tree(self) -> Tree:
        return self.__buffer
    
    def _update_buffer(self, buffer_data: Union[Dict[str, Any], Tree]):
        if isinstance(buffer_data, Tree):
            self.__buffer = buffer_data
        elif isinstance(buffer_data, dict):
            self.__buffer = Tree.to_tree(buffer_data)

    def _handle_exception(self, exception: Exception) -> None:
        """
        Handles exceptions based on the ignore exceptions list.

        Args:
            exception (Exception): The exception to handle.

        Raises:
            Exception: If the exception is not in the ignore exceptions list.
        """
        if not any(isinstance(exception, exc) for exc in self._ignore_exceptions_list):
            raise exception