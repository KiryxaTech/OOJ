# (c) KiryxaTech 2024. Apache License 2.0

import json
from collections import UserDict
from typing import Optional, Union, Dict, List
from pathlib import Path


class JsonBaseClass(UserDict):
    """
    A base class for handling JSON data with optional file operations.

    Attributes:
        data (Optional[Dict]): The JSON data.
        file_path (Optional[Union[Path, str]]): The file path to save the JSON data.
        encoding (Optional[str]): The encoding for the output file.
        indent (Optional[int]): The indentation level for the JSON output.
        ignore_exceptions_list (Optional[List[Exception]]): A list of exceptions to ignore.
    """

    def __init__(self,
                 data: Optional[Dict] = None,
                 file_path: Optional[Union[Path, str]] = None,
                 encoding: Optional[str] = "utf-8",
                 indent: Optional[int] = 4,
                 ignore_exceptions_list: Optional[List[Exception]] = None) -> None:
        """
        Initializes the JsonBaseClass instance.

        Args:
            data (Optional[Dict]): The JSON data. Defaults to an empty dictionary.
            file_path (Optional[Union[Path, str]]): The file path to save the JSON data.
            encoding (Optional[str]): The encoding for the output file. Defaults to "utf-8".
            indent (Optional[int]): The indentation level for the JSON output. Defaults to 4.
            ignore_exceptions_list (Optional[List[Exception]]): A list of exceptions to ignore. Defaults to an empty list.
        """
        super().__init__()
        self._data = data or {}
        self._file_path = file_path
        self._encoding = encoding
        self._indent = indent
        self._ignore_exceptions_list = ignore_exceptions_list or []

    def load(self):
        try:
            with open(self._file_path, 'r', encoding=self._encoding) as file:
                return json.load(file)
        except Exception as e:
            self._handle_exception(e)

    def dump(self, data):
        try:
            with open(self._file_path, 'w', encoding=self._encoding) as file:
                return json.dump(file, data, indent=self._indent)
        except Exception as e:
            self._handle_exception(e)

    def _handle_exception(self, exception: Exception) -> None:
        """
        Handles exceptions based on the ignore exceptions list.

        Args:
            exception (Exception): The exception to handle.

        Raises:
            Exception: If the exception is not in the ignore exceptions list.
        """
        if not any(isinstance(exception, exc) for exc in self._ignore_exceptions_list):
            raise exception