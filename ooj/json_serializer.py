# (c) KiryxaTech, 2024. Apache License 2.0

import json
import jsonschema
from jsonschema.protocols import Validator
from typing import Any, List, Dict, Union, Type
from pathlib import Path

from .json_objects import RootTree


class Field:
    def __init__(self, field_type: Type, types: Dict[str, Any] = None):
        self.field_type = field_type
        self.types = types


class Schema:
    def __init__(self,
                 title: str,
                 type: str = "object",
                 properties: Union[dict, RootTree] = None,
                 required: List[str] = None,
                 version: str = "draft-07") -> None:
        
        self._title = title
        self._type = type
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

    def get(self):
        return self._schema

    @classmethod
    def load_from_file(self, fp: Union[str, Path]) -> 'Schema':
        with open(fp, 'r') as schema_file:
            schema_dict = json.load(schema_file)
        
        Validator.check_schema(schema_dict)

        schema_link: str = schema_dict["$schema"]
        schema_version = schema_link.split("/")[-2]

        schema = Schema(
            title=schema_dict["title"],
            type=schema_dict["type"],
            properties=schema_dict["properties"],
            required=schema_dict["required"],
            version=schema_version
        )

        return schema
    
    def dump_to_file(self, fp: Union[str, Path]) -> None:
        with open(fp, 'w') as schema_file:
            json.dump(self._schema, schema_file, indent=4)


# TODO: Add support for using JSON objects: Root Tree, Tree and Record.
class JsonSerializer:
    def __init__(self, schema: Union[Schema, str]):
        self._schema = schema

    def serialize(self, obj: object, schema_fp: Union[str, Path] = None) -> Dict[str, Any]:
        schema = {"$schema": schema_fp}
        serialized_data = {**schema, **self._serialize(obj)}

        jsonschema.validate(serialized_data, self._schema.get())

        return serialized_data

    def deserialize(self, data: Dict[str, Any], cls: Type, types: Dict[str, Field]) -> object:
        init_args = {}

        for key, field in types.items():
            if isinstance(field, Field):
                if field.types is None:
                    # Если это простое поле
                    init_args[key] = data[key]
                else:
                    if isinstance(data[key], list):
                        # Если это список объектов
                        init_args[key] = [
                            self._deserialize(item, field.field_type, field.types) for item in data[key]
                        ]
                    else:
                        # Если это один вложенный объект
                        init_args[key] = self.deserialize(data[key], field.field_type, field.types)

        return cls(**init_args)

    def _serialize(self, obj: object) -> Dict[str, Any]:
        result = {}

        for key, value in obj.__dict__.items():
            if isinstance(value, (list, tuple)):
                result[key] = [self._serialize(item) for item in value]
            elif hasattr(value, "__dict__"):
                result[key] = self._serialize(value)
            else:
                result[key] = value

        return result