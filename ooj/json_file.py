"""
:authors: KiryxaTech
:license Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2024 KiryxaTech
"""
import json
from typing import Any, Union, Dict, List, Optional
from pathlib import Path
from collections import UserDict
import requests

class JsonFile(UserDict):
    def __init__(self,
                 data: Union[Dict[str, Any], str, Path],
                 save_path: Optional[Union[str, Path]] = None,
                 encoding: Optional[str] = "utf-8",
                 indent: Optional[int] = 4,
                 ignore_errors: Optional[List[Exception]] = None):
        """
        Initialize JsonFile

        :param data: Data to process (dict, file path, or URL)
        :param save_path: Path to save data (if None, data is not saved)
        :param encoding: Encoding for reading/writing files
        :param indent: Indentation for JSON formatting
        :param ignore_errors: List of exceptions to ignore during read/write operations
        """
        super().__init__()
        
        self._save_path = Path(save_path) if save_path else None
        self._encoding = encoding
        self._indent = indent
        self.ignore_errors = ignore_errors or []

        if isinstance(data, dict):
            self.data = data
        elif isinstance(data, (str, Path)):
            if str(data).startswith('http://') or str(data).startswith('https://'):
                self.data = self._load_from_url(data)
            else:
                self._file_path = Path(data)
                self.create_if_not_exists()
                self.data = self.read()
        else:
            raise ValueError("Invalid data type. Must be a dict, file path, or URL.")
        
        if self._save_path:
            self.write(self.data)

    @property
    def save_path(self):
        return self._save_path

    @property
    def exists(self) -> bool:
        return self._save_path.exists() if self._save_path else False

    def create(self):
        if self._save_path:
            self._save_path.parent.mkdir(parents=True, exist_ok=True)
            self._save_path.touch()

    def create_if_not_exists(self):
        if self._save_path and not self._save_path.exists():
            self.create()

    def clear(self):
        super().clear()
        self.write({})

    def delete(self):
        if self._save_path:
            self._save_path.unlink(missing_ok=True)

    def write(self, data: Dict):
        if self._save_path:
            try:
                with self._save_path.open('w', encoding=self._encoding) as f:
                    json.dump(data, f, indent=self._indent)
                self.data = data
            except Exception as e:
                if not self._ignore_exception(e):
                    raise e

    def read(self) -> Dict:
        if not self.exists:
            return {}
        try:
            with self._save_path.open('r', encoding=self._encoding) as f:
                return json.load(f)
        except Exception as e:
            if not self._ignore_exception(e):
                raise e
            return {}

    def set_value(self, keys_path: Union[List[str], str], value: Any) -> None:
        keys_path = [keys_path] if isinstance(keys_path, str) else keys_path
        data = self.data

        def recursive_set(keys, data, value):
            key = keys[0]
            if len(keys) == 1:
                data[key] = value
            else:
                if key not in data or not isinstance(data[key], dict):
                    data[key] = {}
                recursive_set(keys[1:], data[key], value)

        recursive_set(keys_path, data, value)
        self.write(data)
    
    def get_value(self, keys_path: Union[List[str], str]) -> Any:
        keys_path = [keys_path] if isinstance(keys_path, str) else keys_path
        data = self.data

        for key in keys_path:
            if key in data and isinstance(data, dict):
                data = data[key]
            else:
                raise KeyError(f"Key '{key}' not found or is not a dictionary.")
                
        return data

    def remove_key(self, keys_path: Union[List[str], str]):
        keys_path = [keys_path] if isinstance(keys_path, str) else keys_path
        data = self.data

        for key in keys_path[:-1]:
            if key in data and isinstance(data[key], dict):
                data = data[key]
            else:
                raise KeyError(f"Key '{key}' not found or is not a dictionary.")
            
        if keys_path[-1] in data:
            del data[keys_path[-1]]
        else:
            raise KeyError(f"Key '{keys_path[-1]}' not found.")

        self.write(data)

    @classmethod
    def select(cls, file_or_dict: Union['JsonFile', Dict[str, Any]], range_: range) -> Dict[str, Any]:
        data = cls._get_data(file_or_dict)
        selected_data = {k: v for k, v in data.items() if isinstance(v, int) and v in range_}
        return selected_data
    
    @classmethod
    def union(cls, file_or_dict_1: Union['JsonFile', Dict[str, Any]], file_or_dict_2: Union['JsonFile', Dict[str, Any]]) -> Dict[str, Any]:
        data_1 = cls._get_data(file_or_dict_1)
        data_2 = cls._get_data(file_or_dict_2)
        return {**data_1, **data_2}
    
    @classmethod
    def intersect(cls, file_or_dict_1: Union['JsonFile', Dict[str, Any]], file_or_dict_2: Union['JsonFile', Dict[str, Any]]) -> Dict[str, Any]:
        data_1 = cls._get_data(file_or_dict_1)
        data_2 = cls._get_data(file_or_dict_2)
        return {k: v for k, v in data_1.items() if k in data_2 and data_2[k] == v}

    @classmethod
    def _get_data(cls, file_or_dict: Union['JsonFile', Dict[str, Any]]) -> Dict[str, Any]:
        if isinstance(file_or_dict, JsonFile):
            return file_or_dict.data
        elif isinstance(file_or_dict, Dict):
            return file_or_dict
        else:
            raise TypeError("file_or_dict must be an instance of 'JsonFile' or a dictionary.")

    @classmethod
    def from_url(cls, url: str, file_path: Union[str, Path], encoding: Optional[str] = "utf-8", indent: Optional[int] = 4) -> 'JsonFile':
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        instance = cls(file_path, encoding, indent)
        instance.write(data)
        return instance

    def _load_from_url(self, url: str) -> Dict:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            if not self._ignore_exception(e):
                raise e
            return {}

    def _ignore_exception(self, e: Exception) -> bool:
        return any(isinstance(e, ignore_error) for ignore_error in self.ignore_errors)