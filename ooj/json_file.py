"""
:authors: KiryxaTech
:license Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2024 KiryxaTech
"""
import json
from pathlib import Path
from typing import Union, Any, List

from .exceptions import *
from . import *

class JsonFile:
    """ A class for handling JSON file operations. """
    
    def __init__(self, file_path: Union[str, Path], encoding: str = 'utf-8'):
        if not str(file_path).endswith('.json'):
            raise NotJsonFileError(file_path)

        self.file_path = file_path
        self.encoding = encoding
        self.__file = open(file_path, 'r+', encoding=encoding)
        self.__file_dict = {}

    def __reset__(self):
        self.__file = open(self.__file_path, 'r+', encoding=self.encoding)

    def __exit__(self):
        self.__file.close()

    def __del__(self):
        self.__file.close()

    def read(self):
        self.__file_dict = json.load(self.file_path)
    
    def write(self, data):
        json.dump(self.__file_dict, data, ensure_ascii=False, indent=4)

    def add(self, data: KeyValue):
        try:
            self.__file_dict[data.key] = data.value
        except KeyError:
            raise KeyDuplicateError(data.key)
        
        self.save_file()

    def delele(self, key):
        try:
            del self.__file_dict[key]
        except KeyError:
            raise KeyNotFoundError(key)
        
        self.save_file()

    def save_file(self):
        self.write(self.__file_dict)