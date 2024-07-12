"""
:authors: KiryxaTech
:license Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2024 KiryxaTech
"""
import json
from pathlib import Path
from typing import Union, Any, List

class JsonFile:
    def __init__(self,
                 file_path: Union[str, Path],
                 encoding: str = None):
        
        self._path = file_path
        self._encoding = encoding

    @property
    def path(self):
        return self._path
    
    @property
    def encoding(self):
        return self._encoding
    
    def read(self) -> dict:
        with open(self._path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
        
    def write(self, data: dict):
        with open(self._path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)