# (c) KiryxaTech, 2024. Apache License 2.0

import json
from typing import Any, Dict, List, Union
from pathlib import Path

from . import JsonBaseClass
from .exceptions import FileExtensionException


class JsonFile(JsonBaseClass):
    def __init__(self,
                 fp: Union[str, Path],
                 encoding: str = "utf-8",
                 indent: int = 4,
                 ignore_errors: List[Exception] = None):
        """
        Arguments:
        - fp (Union[str, Path]): Path to save data (if None, data is not saved)
        - encoding (str): Encoding for reading/writing files
        - indent (int): Indentation for JSON formatting
        - ignore_errors (List[Exceptions]): List of exceptions to ignore during read/write operations
        """
        super().__init__()
        
        self._fp = Path(fp)
        self._encoding = encoding
        self._indent = indent
        self.ignore_errors = ignore_errors or []

        # Checking the file path for the validity of the extension.
        if not str(self._fp).endswith(".json"):
            self._handle_exception(
                FileExtensionException(f"The file {self.save_path} not JSON file.")
            )
        
        # Buffer for faster access to the dictionary.
        self.__buffer = self.read()

    @property
    def fp(self):
        """ Returns the path to the file. """
        return self._fp

    @property
    def exists(self) -> bool:
        """ Returns True if the file is found, otherwise False. """
        try:
            return self._fp.exists()
        except OSError as e:
            self._handle_exception(e)

    def create(self):
        """ Creates a file anyway. """
        if self._fp:
            try:
                self._fp.parent.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                self._handle_exception(e)

            self._fp.touch()
            self.write({})

    def create_if_not_exists(self):
        """ Creates a file if it does not exist. """
        if not self.exists():
            self.create()

    def delete(self):
        """ Deletes the file anyway. """
        if self._fp:
            try:
                self._fp.unlink(missing_ok=True)
            except FileNotFoundError as e:
                self._handle_exception(e)

    def clear(self):
        """ Cleaning the file. """
        super().clear()
        self.write({})

    def write(self, data: Dict):
        """ Writes a dictionary to a file. """
        if self._fp:
            try:
                with self._fp.open('w', encoding=self._encoding) as f:
                    json.dump(data, f, indent=self._indent)

                self.__update_buffer_from_dict(data)
            except Exception as e:
                self._handle_exception(e)

    def read(self) -> Dict:
        """ Reads data from a file and returns a dictionary. """
        if not self.exists:
            return {}
        try:
            with self._fp.open('r', encoding=self._encoding) as f:
                return json.load(f)
        except Exception as e:
            self._handle_exception(e)
            return {}

    def _normalize_keys(self, keys_path: Union[List[str], str]) -> List[str]:
        """ Checks whether the keys are valid. """
        return [keys_path] if isinstance(keys_path, str) else keys_path

    def _navigate_to_key(self, keys_path: List[str], create_if_missing: bool = False) -> dict:
        """
        Finds the path to the key and creates it
        if the create_if_missing argument = False.
        """
        data = self.__buffer
        for key in keys_path[:-1]:
            if key not in data or not isinstance(data[key], dict):
                if create_if_missing:
                    data[key] = {}
                else:
                    self._handle_exception(KeyError(f"Key '{key}' not found or is not a dictionary."))
            data = data[key]
        return data

    def update_value(self, keys_path: Union[List[str], str], value: Any) -> None:
        """
        Updates the value at the specified key path. If any intermediate keys 
        are missing, they will be created as empty dictionaries.
        
        Arguments:
        - keys_path (Union[List[str], str]): A single key or a list of keys representing 
          the path to the value in the dictionary.
        - value (Any): The value to set at the specified key path.
        """
        keys_path = self._normalize_keys(keys_path)
        data = self._navigate_to_key(keys_path, create_if_missing=True)
        data[keys_path[-1]] = value
        self.write(self.__buffer)

    def fetch_value(self, keys_path: Union[List[str], str]) -> Any:
        """
        Retrieves the value at the specified key path from the internal buffer.
        
        Arguments:
        - keys_path (Union[List[str], str]): A single key or a list of keys representing 
          the path to the value in the dictionary.
        
        Returns:
        - Any: The value at the specified key path.
        
        Raises:
        - KeyError: If the key path does not exist in the data.
        """
        keys_path = self._normalize_keys(keys_path)
        data = self._navigate_to_key(keys_path)
        if keys_path[-1] in data:
            return data[keys_path[-1]]
        self._handle_exception(KeyError(f"Key '{keys_path[-1]}' not found."))

    def delete_key(self, keys_path: Union[List[str], str]) -> None:
        """
        Deletes the value at the specified key path from the internal buffer.
        
        Arguments:
        - keys_path (Union[List[str], str]): A single key or a list of keys representing 
          the path to the value in the dictionary.
        
        Raises:
        - KeyError: If the key path does not exist in the data.
        """
        keys_path = self._normalize_keys(keys_path)
        data = self._navigate_to_key(keys_path)
        if keys_path[-1] in data:
            del data[keys_path[-1]]
        else:
            self._handle_exception(KeyError(f"Key '{keys_path[-1]}' not found."))
        self.write(self.__buffer)

    def update_buffer_from_file(self):
        """
        Updates the internal buffer by reading the current data from the file.
        This is useful if the file has been changed externally and the buffer 
        needs to be synced with the file.
        """
        self.__buffer = self.read()

    def _handle_exception(self, e: Exception):
        """
        Handles exceptions during file operations. If the exception is one of
        those specified in `ignore_errors`, the exception will be raised.
        
        Arguments:
        - e (Exception): The exception to be handled.
        """
        if any(isinstance(e, ignore_error) for ignore_error in self.ignore_errors):
            raise e

    def __update_buffer_from_dict(self, dictionary: Dict):
        """
        Updates the internal buffer with the given dictionary.
        
        Arguments:
        - dictionary (Dict): The dictionary to update the buffer with.
        """
        self.__buffer = dictionary
