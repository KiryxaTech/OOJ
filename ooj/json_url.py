import re
import requests
import json
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
                 ignore_exceptions_list: Optional[List[Exception]] = None):
        
        super().__init__()

        self._url = url
        self._output_file_path = output_file_path
        self._encoding = encoding
        self._indent = indent
        self._ignore_exceptions_list = ignore_exceptions_list or []

        self.__validate_url()

    def load_from_url(self) -> Dict:
        try:
            response = requests.get(self._url)
            response.raise_for_status()

            data = response.json()
            self.dump_to_file(data)

            return data
        except Exception as e:
            self.__handle_exception(e)

            self.dump_to_file({})
            return {}

    def dump_to_file(self, data: Dict) -> None:
        # Проверка и создание директорий
        output_path = Path(self._output_file_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding=self._encoding) as file:
            json.dump(data, file, indent=self._indent)

    def to_json_file(self) -> JsonFile:
        data = self.load_from_url()
        json_file = JsonFile(
            data=data,
            save_path=self._output_file_path,
            encoding=self._encoding,
            indent=self._indent,
            ignore_errors=self._ignore_exceptions_list
        )
        return json_file

    def __validate_url(self) -> None:
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain name
            r'localhost|' # or localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # or IPv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # or IPv6
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$',
            re.IGNORECASE
        )

        if not re.match(regex, self._url):
            self.__handle_exception(ValueError(f"Invalid URL: {self._url}"))

    def __handle_exception(self, exception: Exception) -> None:
        if not any(isinstance(exception, exc) for exc in self._ignore_exceptions_list):
            raise exception
