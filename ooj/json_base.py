# (c) KiryxaTech 2024. Apache License 2.0

from abc import ABC, abstractmethod
from typing import Any, Dict, Union

from .json_objects import RootTree, TreeConverter


class Readable(ABC):
    def __init__(self, fp: str):
        self._fp = fp

    @abstractmethod
    def read(self): pass


class Writable(ABC):
    def __init__(self, fp: str) -> None:
        self._fp = fp

    def write(self, data: Union[Dict[str, Any], RootTree]): pass


class JsonBase(ABC):
    """
    A base class for handling JSON data with optional file operations.

    Attributes:
        data (Dict[str, Any]): The JSON data.
    """

    def __init__(self, data: Union[Dict[str, Any], RootTree]):
        """
        Initializes the JsonBaseClass instance.

        Args:
            data (Dict[str, Any]): The JSON data. Defaults to an empty dictionary.
        """
        self.__buffer: RootTree = None

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
        return TreeConverter.to_dict(self.__buffer)

    def get_buffer_tree(self) -> RootTree:
        return self.__buffer
    
    def _update_buffer(self, buffer_data: Union[Dict[str, Any], RootTree]):
        if isinstance(buffer_data, RootTree):
            self.__buffer = buffer_data
        elif isinstance(buffer_data, dict):
            self.__buffer = TreeConverter.to_root_tree(buffer_data)

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