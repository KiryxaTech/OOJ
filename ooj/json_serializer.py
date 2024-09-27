# (c) KiryxaTech, 2024. Apache License 2.0

import json
import jsonschema
from jsonschema.protocols import Validator
from typing import Any, List, Dict, Union, Type, get_args
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


class JsonSerializer:
    def __init__(self, schema: Union[Schema, str] = None):
        self._schema = schema
    
    def serialize(self,
                  obj: object,
                  schema_file_path: Union[str, Path] = None) -> Dict[str, Any]:
        
        seria = {}
        if not schema_file_path is None:
            seria["$schema"] = schema_file_path
        
        object_items = obj.__dict__.items()
        for field_name, field_value in object_items:
            if self.is_array(field_value):
                seria[field_name] = [self.serialize(item) for item in field_value]
            elif self.is_object(field_value):
                seria[field_name] = self.serialize(field_value)
            else:
                seria[field_name] = field_value

        if not schema_file_path is None:
            self.validate(seria, schema_file_path)
        
        return seria

    def deserialize(self,
                    seria: Union[Dict[str, Any], RootTree],
                    seria_class: Type,
                    seria_fields_types: Dict[str, Union[Type, Field]] = None) -> object:
        
        try:
            seria.pop("$schema")
        except: pass

        parameters = {}
        for key, value in seria.items():
            print(f"Тип значения: {type(value)}")  # Вывод типа данных

            if self.is_dict(value):
                if isinstance(seria_fields_types[key], Field):
                    nested_class = seria_fields_types[key].field_type
                    nested_fields_types = seria_fields_types[key].types
                else:
                    nested_class = seria_fields_types[key]
                    nested_fields_types = None
                
                parameters[key] = self.deserialize(value, nested_class, nested_fields_types)

            elif self.is_array(value):
                parameters[key] = []
                array_item_type = get_args(seria_fields_types[key].field_type)[0]
                for item in value:
                    parameters[key].append(
                        self.deserialize(item, array_item_type, seria_fields_types[key].types)
                    )
            else:
                parameters[key] = value

        return seria_class(**parameters)

    def is_array(self, value: Any):
        return isinstance(value, (list, tuple))
    
    def is_object(self, value: Any):
        return hasattr(value, "__dict__")
    
    def is_dict(self, value):
        return isinstance(value, dict)
    
    def validate(self,
                 seria: Dict[str, Any],
                 schema_file_path: Union[str, Path]):
        
        with open(schema_file_path, 'r') as file:
            schema = json.load(file)

        Validator.check_schema(schema)
        jsonschema.validate(seria, schema)