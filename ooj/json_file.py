# (c) KiryxaTech 2024. Apache License 2.0

import json
import pathlib
from typing import Any, Union, Dict, List, Optional
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
        Initialize JsonFile

        :param fp: Path to save data (if None, data is not saved)
        :param encoding: Encoding for reading/writing files
        :param indent: Indentation for JSON formatting
        :param ignore_errors: List of exceptions to ignore during read/write operations
        """
        super().__init__()
        
        self._fp = Path(fp)
        self._encoding = encoding
        self._indent = indent
        self.ignore_errors = ignore_errors or []

        if not str(self._fp).endswith(".json"):
            self._handle_exception(
                FileExtensionException(f"The file {self.save_path} not JSON file.")
            )
        
        # Buffer for faster access to the dictionary.
        self.__buffer = self.read()

    @property
    def fp(self):
        return self._fp

    @property
    def exists(self) -> bool:
        try:
            return self._fp.exists()
        except OSError as e:
            self._handle_exception(e)

    def create(self):
        if self._fp:
            try:
                self._fp.parent.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                self._handle_exception(e)

            self._fp.touch()
            self.write({})

    def create_if_not_exists(self):
        if not self.exists():
            self.create()

    def delete(self):
        if self._fp:
            try:
                self._fp.unlink(missing_ok=True)
            except FileNotFoundError as e:
                self._handle_exception(e)

    def clear(self):
        super().clear()
        self.write({})

    def write(self, data: Dict):
        if self._fp:
            try:
                with self._fp.open('w', encoding=self._encoding) as f:
                    json.dump(data, f, indent=self._indent)

                self.__update_buffer_from_dict(data)
            except Exception as e:
                self._handle_exception(e)

    def read(self) -> Dict:
        if not self.exists:
            return {}
        try:
            with self._fp.open('r', encoding=self._encoding) as f:
                return json.load(f)
        except Exception as e:
            self._handle_exception(e)
            return {}

    def _normalize_keys(self, keys_path: Union[List[str], str]) -> List[str]:
        return [keys_path] if isinstance(keys_path, str) else keys_path

    def _navigate_to_key(self, keys_path: List[str], create_if_missing: bool = False) -> dict:
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
        keys_path = self._normalize_keys(keys_path)
        data = self._navigate_to_key(keys_path, create_if_missing=True)
        data[keys_path[-1]] = value
        self.write(self.__buffer)

    def fetch_value(self, keys_path: Union[List[str], str]) -> Any:
        keys_path = self._normalize_keys(keys_path)
        data = self._navigate_to_key(keys_path)
        if keys_path[-1] in data:
            return data[keys_path[-1]]
        self._handle_exception(KeyError(f"Key '{keys_path[-1]}' not found."))

    def delete_key(self, keys_path: Union[List[str], str]) -> None:
        keys_path = self._normalize_keys(keys_path)
        data = self._navigate_to_key(keys_path)
        if keys_path[-1] in data:
            del data[keys_path[-1]]
        else:
            self._handle_exception(KeyError(f"Key '{keys_path[-1]}' not found."))
        self.write(self.__buffer)

    def update_buffer_from_file(self):
        self.__buffer = self.read()

    def __update_buffer_from_dict(self, dictionary: Dict):
        self.__buffer = dictionary

    # @classmethod
    # def select(cls, file_or_dict: Union['JsonFile', Dict[str, Any]], range_: range) -> Dict[str, Any]:
    #     data = cls._get_data(file_or_dict)
    #     selected_data = {k: v for k, v in data.items() if isinstance(v, int) and v in range_}
    #     return selected_data
    
    # @classmethod
    # def union(cls, file_or_dict_1: Union['JsonFile', Dict[str, Any]], file_or_dict_2: Union['JsonFile', Dict[str, Any]]) -> Dict[str, Any]:
    #     data_1 = cls._get_data(file_or_dict_1)
    #     data_2 = cls._get_data(file_or_dict_2)
    #     return {**data_1, **data_2}
    
    # @classmethod
    # def intersect(cls, file_or_dict_1: Union['JsonFile', Dict[str, Any]], file_or_dict_2: Union['JsonFile', Dict[str, Any]]) -> Dict[str, Any]:
    #     data_1 = cls._get_data(file_or_dict_1)
    #     data_2 = cls._get_data(file_or_dict_2)
    #     return {k: v for k, v in data_1.items() if k in data_2 and data_2[k] == v}

    @classmethod
    def _get_data(cls, file_or_dict: Union['JsonFile', Dict[str, Any]]) -> Dict[str, Any]:
        if isinstance(file_or_dict, JsonFile):
            return file_or_dict.data
        elif isinstance(file_or_dict, Dict):
            return file_or_dict
        else:
            raise TypeError("file_or_dict must be an instance of 'JsonFile' or a dictionary.")

    def _handle_exception(self, e: Exception):
        if any(isinstance(e, ignore_error) for ignore_error in self.ignore_errors):
            raise e