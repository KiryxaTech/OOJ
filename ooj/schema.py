# (c) KiryxaTech, 2024. Apache License 2.0

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from jsonschema.protocols import Validator


class Schema:
    """
    A class representing a JSON Schema.

    Attributes:
        title (str): The title of the schema.
        type_ (Optional[str]): The type of the schema. Defaults to "object".
        properties (Optional[Dict[str, Any]]): The properties of the schema.
        required (Optional[List[str]]): The required properties of the schema.
        version (Optional[str]): The version of the schema. Defaults to "draft-07".
        _schema (Dict[str, Any]): The internal representation of the JSON schema.

    Methods:
        to_dict() -> Dict[str, Any]:
            Converts the schema to a dictionary format.
        
        load_from_file(file_path: Union[str, Path]) -> 'Schema':
            Loads a schema from a JSON file and returns a Schema instance.
        
        dump_to_file(file_path: Union[str, Path]) -> None:
            Dumps the schema to a JSON file.
        
        _get_version(schema_link: str) -> str:
            Extracts the version from the schema link.
    """

    def __init__(
        self,
        title: str,
        type_: Optional[str] = "object",
        properties: Optional[Dict[str, Any]] = None,
        required: Optional[List[str]] = None,
        version: Optional[str] = "draft-07"
    ) -> None:
        """Initializes a Schema instance with the provided attributes.

        Args:
            title (str): The title of the schema.
            type_ (Optional[str]): The type of the schema. Defaults to "object".
            properties (Optional[Dict[str, Any]]): The properties of the schema. Defaults to an empty dictionary.
            required (Optional[List[str]]): The required properties of the schema. Defaults to an empty list.
            version (Optional[str]): The version of the schema. Defaults to "draft-07".
        """
        
        self._title = title
        self._type = type_
        self._properties = properties or {}
        self._version = version
        self._required = required or []

        self._schema = {
            "$schema": f"http://json-schema.org/{version}/schema#",
            "title": self._title,
            "type": self._type,
            "properties": self._properties,
            "required": self._required
        }

    def to_dict(self) -> Dict[str, Any]:
        """Converts the schema to a dictionary format.
        
        Returns:
            Dict[str, Any]: The JSON schema as a dictionary.
        """
        return self._schema

    @classmethod
    def load_from_file(cls, file_path: Union[str, Path]) -> 'Schema':
        """Loads a schema from a JSON file and returns a Schema instance.

        Args:
            file_path (Union[str, Path]): The path to the JSON file containing the schema.

        Returns:
            Schema: A Schema instance representing the loaded schema.
        """
        with open(file_path, 'r') as schema_file:
            schema_dict = json.load(schema_file)
        
        Validator.check_schema(schema_dict)

        schema = Schema(
            title=schema_dict["title"],
            type_=schema_dict["type"],
            properties=schema_dict["properties"],
            required=schema_dict["required"],
            version=cls._get_version(schema_dict["$schema"])
        )

        return schema
    
    def dump_to_file(self, file_path: Union[str, Path]) -> None:
        """Dumps the schema to a JSON file.

        Args:
            file_path (Union[str, Path]): The path to the JSON file where the schema will be dumped.
        """
        with open(file_path, 'w') as schema_file:
            json.dump(self._schema, schema_file, indent=4)

    def _get_version(self, schema_link: str) -> str:
        """Extracts the version from the schema link.

        Args:
            schema_link (str): The schema link from which to extract the version.

        Returns:
            str: The extracted version of the schema.
        """
        SCHEMA_VERSION_INDEX = -2
        schema_version = schema_link.split('/')[SCHEMA_VERSION_INDEX]
        return schema_version