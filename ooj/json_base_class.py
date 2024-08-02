# (c) KiryxaTech 2024. Apache License 2.0

from collections import UserDict
from typing import Optional, Union, Dict, List
from pathlib import Path


class JsonBaseClass(UserDict):
    def __init__(self,
                 data: Optional[Dict] = {},
                 file_path: Optional[Union[Path, str]] = None,
                 encoding: Optional[str] = "utf-8",
                 indent: Optional[int] = 4,
                 ignore_exceptions_list: Optional[List[Exception]] = []) -> None:
        
        super().__init__()

        self._data = data
        self._file_path = file_path
        self._encoding = encoding
        self._indent = indent
        self._ignore_exceptions_list = ignore_exceptions_list