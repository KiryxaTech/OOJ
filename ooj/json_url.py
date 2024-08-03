# (c) KiryxaTech 2024. Apache License 2.0

import re
import requests
import json
from typing import Union, Optional, List, Dict
from pathlib import Path

from . import JsonBaseClass, JsonFile


class JsonURL(JsonBaseClass):
    """
    A class to load JSON data from a URL and optionally save it to a file.

    Attributes:
        url (str): The URL to fetch JSON data from.
        output_file_path (Optional[Union[Path, str]]): The file path to save the JSON data.
        encoding (Optional[str]): The encoding for the output file.
        indent (Optional[int]): The indentation level for the JSON output.
        ignore_exceptions_list (Optional[List[Exception]]): A list of exceptions to ignore.
    """

    def __init__(self,
                 url: str,
                 output_file_path: Optional[Union[Path, str]] = None,
                 encoding: Optional[str] = "utf-8",
                 indent: Optional[int] = 4,
                 ignore_exceptions_list: Optional[List[Exception]] = None):
        """
        Initializes the JsonURL instance.

        Args:
            url (str): The URL to fetch JSON data from.
            output_file_path (Optional[Union[Path, str]]): The file path to save the JSON data.
            encoding (Optional[str]): The encoding for the output file. Defaults to "utf-8".
            indent (Optional[int]): The indentation level for the JSON output. Defaults to 4.
            ignore_exceptions_list (Optional[List[Exception]]): A list of exceptions to ignore. Defaults to an empty list.
        """
        self._url = url
        self._validate_url()

        super().__init__(
            data=None,
            file_path=output_file_path,
            encoding=encoding,
            indent=indent,
            ignore_exceptions_list=ignore_exceptions_list or []
        )

        self._data = self.load_from_url()

    def load_from_url(self) -> Dict:
        """
        Loads JSON data from the URL.

        Returns:
            Dict: The JSON data loaded from the URL.

        Raises:
            Exception: If an error occurs and it is not in the ignore exceptions list.
        """
        if self._data is not None:
            return self._data
        try:
            response = requests.get(self._url)
            response.raise_for_status()

            self._data = response.json()
            self._dump_to_file(self._data)

            return self._data
        except Exception as e:
            self._handle_exception(e)
            self._dump_to_file({})
            return {}

    def _dump_to_file(self, data: Dict) -> None:
        """
        Dumps JSON data to a file.

        Args:
            data (Dict): The JSON data to be saved.
        """
        if self._file_path:
            with open(self._file_path, 'w', encoding=self._encoding) as f:
                json.dump(data, f, indent=self._indent)

    def to_json_file(self) -> JsonFile:
        """
        Converts the JSON data to a JsonFile instance.

        Returns:
            JsonFile: An instance of JsonFile containing the JSON data.
        """
        json_file = JsonFile(
            data=self.load_from_url(),
            save_path=self._file_path,
            encoding=self._encoding,
            indent=self._indent,
            ignore_errors=self._ignore_exceptions_list
        )
        return json_file

    def _validate_url(self) -> None:
        """
        Validates the URL.

        Raises:
            ValueError: If the URL is invalid.
        """
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain name
            r'localhost|'  # or localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # or IPv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # or IPv6
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$',
            re.IGNORECASE
        )

        if not re.match(regex, self._url):
            self._handle_exception(ValueError(f"Invalid URL: {self._url}"))