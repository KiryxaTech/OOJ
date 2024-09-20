# (c) KiryxaTech, 2024. Apache License 2.0

import json
from typing import Any, Dict, List, Union
from pathlib import Path

from .json_base import JsonBase, Readable, Writable
from .json_objects import RootTree, Entry, TreeConverter
from .exceptions import FileExtensionException


class JsonFile(JsonBase, Readable, Writable):
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
        
        self._fp = Path(fp)
        self._encoding = encoding
        self._indent = indent
        self.ignore_errors = ignore_errors or []

        JsonBase.__init__(self, {})
        Readable.__init__(self, self._fp)
        Readable.__init__(self, self._fp)

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
        if not self.exists:
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
        self.write({})

    def write(self, data: Union[Dict, RootTree]):
        """ Writes a dictionary to a file. """
        if self._fp:
            try:
                with self._fp.open('w', encoding=self._encoding) as f:
                    if isinstance(data, RootTree):
                        data = data.to_dict()
                    elif not isinstance(data, dict):
                        self._handle_exception(TypeError(f'Type {type(data)} not supported in write method.'))
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
        
    def read_tree(self) -> RootTree:
        json_data = self.read()
        return TreeConverter.to_root_tree(json_data)


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

    def set_entry(self, key_s: Union[List[str], str], value: Union[Any, Entry, RootTree]) -> None:
        """
        Updates the value at the specified key path. If any intermediate keys 
        are missing, they will be created as empty dictionaries.
        
        Arguments:
        - key_s (Union[List[str], str]): A single key or a list of keys representing 
        the path to the value in the dictionary.
        - value (Union[Any, Entry, Tree]): The value or Entry/Tree object to set at the specified key path.
        """
        key_s = self._normalize_keys(key_s)
        
        if isinstance(value, (Entry, RootTree)):
            value = value.to_dict()

        data = self._navigate_to_key(key_s, create_if_missing=True)
        data[key_s[-1]] = value
        self.write(self.__buffer)

    def get_entry(self, key_s: Union[List[str], str]) -> Any:
        key_s = self._normalize_keys(key_s)
        data = self._navigate_to_key(key_s)
        if key_s[-1] in data:
            return data[key_s[-1]]
        self._handle_exception(KeyError(f"Key '{key_s[-1]}' not found."))

    def del_entry(self, key_s: Union[List[str], str]) -> None:
        key_s = self._normalize_keys(key_s)
        data = self._navigate_to_key(key_s)
        if key_s[-1] in data:
            del data[key_s[-1]]
        else:
            self._handle_exception(KeyError(f"Key '{key_s[-1]}' not found."))
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