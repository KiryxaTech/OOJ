from collections import UserDict
from pathlib import Path
from typing import Union, Optional, List, Dict

from . import JsonFile


class JsonURL(UserDict):
    def __init__(self,
                 url: str,
                 output_file_path: Optional[Union[Path, str]] = None,
                 encoding: Optional[str] = "utf-8",
                 indent: Optional[int] = 4,
                 ignore_exceptions_list: Optional[List[Exception]] = []):
        
        super().__init__()

        self._url = url
        self._output_file_path = output_file_path
        self._encoding = encoding
        self._indent = indent
        self._ignore_exceptions_list = ignore_exceptions_list

        self.__validate_url()

    def load(self) -> Dict:
        pass

    def dump(self, data: Dict) -> None:
        pass

    def to_json_file(self) -> JsonFile:
        pass

    def __validate_url(self) -> None:
        pass

    def __handle_exception(self) -> None:
        pass