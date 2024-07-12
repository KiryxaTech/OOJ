"""
:authors: KiryxaTech
:license Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2024 KiryxaTech
"""
import json
from pathlib import Path
from typing import Union

class key:
    def __init__(self, id, value):
        self._id = key
        self.value = value

    @property
    def id(self):
        return self._key


class JsonFile:
    def __init__(self,
                 file_path: Union[str, Path],
                 encoding: str = 'utf-8'):
        
        self._path = file_path
        self._encoding = encoding
        self._dict = {}

        self._update_dict()

    @property
    def path(self):
        return self._path
    
    @property
    def encoding(self):
        return self._encoding

    def read(self) -> dict:
        with open(self._path, 'r', encoding=self._encoding) as json_file:
            return json.load(json_file)
        
    def write(self, data: dict):
        with open(self._path, 'w', encoding=self._encoding) as json_file:
            json.dump(data, json_file, indent=4)

    def add(self, value, *keys):
        d = self._dict
        for key in keys[:-1]:
            if key not in d or not isinstance(d[key], dict):
                d[key] = {}
                d = d[key]
            else:
                return
            
            d[keys[-1]] = value

        self._push_dict_changes()
        self._update_dict()

    def remove(self, *keys):
        d = self._dict
        for key in keys[:-1]:
            if key in d and isinstance(d[key], dict):
                d = d[key]
            else:
                return
            
        if keys[-1] in d:
            del d[keys[-1]]
        
        self._push_dict_changes()
        self._update_dict()

    def _update_dict(self):
        self._dict = self.read()

    def _push_dict_changes(self):
        self.write(self._dict)