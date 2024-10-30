# (c) KiryxaTech, 2024. Apache License 2.0. See the LICENSE file.

import json
from typing import Any, Dict, List, Union
from pathlib import Path

from ooj.base import JsonBase, Readable, Writable
from ooj.core_classes import Entry, Tree, TreeConverter
from ooj.exceptions import FileExtensionException


class JsonFile(JsonBase, Readable, Writable):
    """
    JsonFile manages JSON file operations, supporting structured access, manipulation, 
    and conversion of data into `Tree` and `Entry` objects for complex JSON handling.

    Attributes:
        _fp (Path): The file path for storing JSON data.
        _encoding (str): Encoding for reading and writing files (default "utf-8").
        _indent (int): Indentation level for JSON formatting.
        ignore_errors (List[Exception]): List of exceptions to ignore during read/write.

    Methods:
        create():
            Ensures the file is created with initial empty JSON data.

        create_if_not_exists():
            Creates the file only if it does not already exist.

        delete():
            Deletes the file from the system.

        clear():
            Clears all data in the file by writing an empty JSON object.

        write(data: Union[Dict, Tree]):
            Writes JSON data or a `Tree` object to the file.

        read() -> Dict:
            Reads and returns JSON data from the file as a dictionary.

        read_tree() -> Tree:
            Reads data from the file and converts it into a `Tree` structure.

        set_entry(key_s: Union[List[str], str], value: Union[Any, Entry, Tree]):
            Sets a value at a specified key path, creating intermediate keys as needed.

        get_entry(key_s: Union[List[str], str]) -> Any:
            Retrieves a value at the specified key path.

        del_entry(key_s: Union[List[str], str]):
            Deletes an entry at the specified key path.

        update_buffer_from_file():
            Refreshes the internal buffer with the current data from the file.
    """

    def __init__(self,
                 fp: Union[str, Path],
                 encoding: str = "utf-8",
                 indent: int = 4,
                 ignore_errors: List[Exception] = None):
        """
        Initializes the JsonFile instance with the specified file path, encoding, 
        and error-handling options.

        Args:
            fp (Union[str, Path]): File path for storing JSON data.
            encoding (str): Encoding for file operations (default "utf-8").
            indent (int): JSON indentation level (default 4).
            ignore_errors (List[Exception], optional): List of exceptions to ignore.
        """
        self._fp = Path(fp)
        self._encoding = encoding
        self._indent = indent
        self.ignore_errors = ignore_errors or []

        JsonBase.__init__(self, {})
        Readable.__init__(self, self._fp)
        Writable.__init__(self, self._fp)

        if not str(self._fp).endswith(".json"):
            self._handle_exception(
                FileExtensionException(f"The file {self.save_path} is not a JSON file.")
            )
        
        self.__buffer = {}
        if self.exists:
            self.update_buffer_from_file()

    @property
    def fp(self):
        """ Returns the path to the JSON file. """
        return self._fp

    @property
    def exists(self) -> bool:
        """ Returns True if the file exists; otherwise, False. """
        try:
            return self._fp.exists()
        except OSError as e:
            self._handle_exception(e)

    def create(self):
        """ Ensures the file is created and initialized with empty JSON data. """
        if self._fp:
            try:
                self._fp.parent.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                self._handle_exception(e)
            self._fp.touch()
            self.write({})

    def create_if_not_exists(self):
        """ Creates the file only if it does not already exist. """
        if not self.exists:
            self.create()

    def delete(self):
        """ Deletes the JSON file. """
        if self._fp:
            try:
                self._fp.unlink(missing_ok=True)
            except FileNotFoundError as e:
                self._handle_exception(e)

    def clear(self):
        """ Clears all data in the file by writing an empty JSON object. """
        self.write({})

    def write(self, data: Union[Dict, Tree]):
        """
        Writes data to the file. Accepts either a dictionary or `Tree` instance.

        Args:
            data (Union[Dict, Tree]): JSON-compatible dictionary or `Tree` object.
        """
        if self._fp:
            try:
                with self._fp.open('w', encoding=self._encoding) as f:
                    if isinstance(data, Tree):
                        data = data.to_dict()
                    elif not isinstance(data, dict):
                        self._handle_exception(TypeError(f'Type {type(data)} not supported in write method.'))
                    json.dump(data, f, indent=self._indent)

                self.__update_buffer_from_dict(data)
            except Exception as e:
                self._handle_exception(e)

    def read(self) -> Dict:
        """ Reads and returns JSON data from the file as a dictionary. """
        if not self.exists:
            return {}
        try:
            with self._fp.open('r', encoding=self._encoding) as f:
                return json.load(f)
        except Exception as e:
            self._handle_exception(e)
            return {}
        
    def read_tree(self) -> Tree:
        """
        Reads data from the file and converts it to a `Tree` structure.

        Returns:
            Tree: An instance representing the file's JSON data as a tree structure.
        """
        json_data = self.read()
        return TreeConverter.to_tree(json_data)

    def _normalize_keys(self, keys_path: Union[List[str], str]) -> List[str]:
        """ Ensures keys are in a list format for consistent access. """
        return [keys_path] if isinstance(keys_path, str) else keys_path

    def _navigate_to_key(self, keys_path: List[str], create_if_missing: bool = False) -> dict:
        """
        Navigates to the specified key path, optionally creating intermediate paths.

        Args:
            keys_path (List[str]): List of keys representing the path.
            create_if_missing (bool): Whether to create missing intermediate keys.

        Returns:
            dict: The dictionary at the last key in the path.
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

    def set_entry(self, key_s: Union[List[str], str], value: Union[Any, Entry, Tree]) -> None:
        """
        Sets a value at a specified key path, creating intermediate keys if needed.

        Args:
            key_s (Union[List[str], str]): Path to the key as a list or string.
            value (Union[Any, Entry, Tree]): Value or object to assign at the path.
        """
        key_s = self._normalize_keys(key_s)
        
        if isinstance(value, (Entry, Tree)):
            value = value.to_dict()

        data = self._navigate_to_key(key_s, create_if_missing=True)
        data[key_s[-1]] = value
        self.write(self.__buffer)

    def get_entry(self, key_s: Union[List[str], str]) -> Any:
        """
        Retrieves the value at the specified key path.

        Args:
            key_s (Union[List[str], str]): Path to the key as a list or string.

        Returns:
            Any: The value at the specified key.
        """
        key_s = self._normalize_keys(key_s)
        data = self._navigate_to_key(key_s)
        if key_s[-1] in data:
            return data[key_s[-1]]
        self._handle_exception(KeyError(f"Key '{key_s[-1]}' not found."))

    def del_entry(self, key_s: Union[List[str], str]) -> None:
        """
        Deletes the entry at the specified key path.

        Args:
            key_s (Union[List[str], str]): Path to the key as a list or string.
        """
        key_s = self._normalize_keys(key_s)
        data = self._navigate_to_key(key_s)
        if key_s[-1] in data:
            del data[key_s[-1]]
        else:
            self._handle_exception(KeyError(f"Key '{key_s[-1]}' not found."))
        self.write(data)

    def update_buffer_from_file(self):
        """ Syncs the internal buffer with the current data in the file. """
        self.__buffer = self.read()

    def _handle_exception(self, e: Exception):
        """
        Manages exceptions, raising only if not in ignore_errors.

        Args:
            e (Exception): The exception to handle.
        """
        if not any(isinstance(e, ignore_error) for ignore_error in self.ignore_errors):
            raise e

    def __update_buffer_from_dict(self, dictionary: Dict):
        """
        Updates the buffer with a new dictionary.

        Args:
            dictionary (Dict): Dictionary to update the buffer.
        """
        self.__buffer.update(dictionary)