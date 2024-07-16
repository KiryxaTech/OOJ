"""
:authors: KiryxaTech
:license Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2024 KiryxaTech
"""
import json
from typing import Any, Union, Dict, List, Optional, overload
import os
from pathlib import Path

class JsonFile:
    def __init__(self,
                 file_path: Union[str, Path],
                 encoding: Optional[str] = "utf-8",
                 indent: Optional[int] = 4,
                 ignore_errors: Optional[List[Exception]] = None):
        
        self._file_path = file_path
        self._encoding = encoding
        self._indent = indent

        self.create_if_not_exists()

    @property
    def file_path(self):
        return self._file_path

    @property
    def exists(self) -> bool:
        return os.path.exists(self._file_path)

    def create(self):
        dirs = str(self._file_path).split("\\")[0:-1]
        dirs_path = "\\".join(dirs)
        if not os.path.exists(dirs_path):
            os.mkdir(dirs_path)

        with open(self._file_path, 'w', encoding=self._encoding) as f:
            json.dump({}, f)

    def create_if_not_exists(self):
        if not os.path.exists(self._file_path):
            self.create()

    def clear(self):
        self.write({})

    def delete(self):
        os.remove(self._file_path)

    def write(self, data: Dict):
        with open(self._file_path, 'w', encoding=self._encoding) as f:
            json.dump(data, f, indent=self._indent)

    def read(self) -> Dict:
        with open(self._file_path, 'r', encoding=self._encoding) as f:
            return json.load(f)

    @overload
    def set_value(self, key: str, value) -> None: ...

    @overload
    def set_value(self, keys: List[str], value) -> None: ...

    def set_value(self, keys_path: Union[List[str], str], value: Any) -> None:
        data = self.read()

        def recursive_set(keys, data, value):
            key = keys[0]
            if len(keys) == 1:
                data[key] = value
            else:
                if key not in data or not isinstance(data[key], dict):
                    data[key] = {}
                recursive_set(keys[1:], data[key], value)

        if isinstance(keys_path, str):
            data[keys_path] = value
        elif isinstance(keys_path, list):
            if keys_path[0] not in data or not isinstance(data[keys_path[0]], dict):
                data[keys_path[0]] = {}
            recursive_set(keys_path[1:], data[keys_path[0]], value)
        
        self.write(data)
    
    @overload
    def get_value(self, key: str) -> Any: ...

    @overload
    def get_value(self, keys: List[str]) -> Any: ...

    def get_value(self, keys_path: Union[List[str], str]) -> Any:
        data = self.read()

        if isinstance(keys_path, str):
            return data[keys_path]

        for key in keys_path[:-1]:
            if key in data and isinstance(data[key], dict):
                data = data[key]
            else:
                raise KeyError(f"Key '{key}' not found or is not a dictionary.")
                
        if keys_path[-1] in data:
            return data[keys_path[-1]]
        else:
            raise KeyError(f"Key '{keys_path[-1]}' not found.")

    @overload
    def remove_key(self, key: str) -> None: ...

    @overload
    def remove_key(self, keys: List[str]) -> None: ...

    def remove_key(self, keys_path: Union[List[str], str]):
        data = self.read()
            
        if isinstance(keys_path, str):
            del data[keys_path]
        elif isinstance(keys_path, list):
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