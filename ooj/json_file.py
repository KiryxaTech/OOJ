"""
:authors: KiryxaTech
:license Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2024 KiryxaTech
"""
import json
from pathlib import Path
from typing import Union, Dict


class JsonFile:
    def __init__(self, file_path: Union[str, Path], encoding: str = 'utf-8'):
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

    def union(self, file_or_dict: Union['JsonFile', Dict]):
        union_dict = self._dict

        if isinstance(file_or_dict, JsonFile):
            file_or_dict = file_or_dict.read()
        if isinstance(file_or_dict, Dict):
            union_dict.update(file_or_dict)
            self._push_dict_changes()
            self._update_dict()

        return union_dict

    def intersect(self, file_or_dict: Union['JsonFile', Dict]):
        if isinstance(file_or_dict, JsonFile):
            file_or_dict = file_or_dict.read()
        
        intersect_dict = {}
        for key in file_or_dict:
            if key in self._dict:
                intersect_dict[key] = self.read()[key]
        
        return intersect_dict

    def select(self, select_list):
        select_dict = {}

        for key, value in self._dict.items():
            if value in select_list:
                select_dict[key] = value

        return select_dict


    def _update_dict(self):
        self._dict = self.read()

    def _push_dict_changes(self):
        self.write(self._dict)