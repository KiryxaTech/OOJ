# (c) KiryxaTech, 2024. Apache License 2.0

import json
from pathlib import Path
from typing import Any, Dict, List, Type, Optional, Union, get_args

import jsonschema
from jsonschema.protocols import Validator

from .json_objects import RootTree


class Field:
    def __init__(self, type_: Type, types: Optional[Dict[str, Union[Type, 'Field']]] = None):
        self.type = type_
        self.types = types

    @classmethod
    def wrap_type(cls, type: Union[Type, 'Field']) -> 'Field':
        if isinstance(type, Field):
            return type
        return Field(type)
    
    @classmethod
    def wrap_all_types(cls, types: Dict[str, Union[Type, 'Field']]) -> Dict[str, 'Field']:
        wrapped_types = {}
        for key, type_ in types.items():
            wrapped_types[key] = cls.wrap_type(type_)

        return wrapped_types


class Schema:
    def __init__(
        self,
        title: str,
        type_: Optional[str] = "object",
        properties: Optional[Dict[str, Any]] = None,
        required: Optional[List[str]] = None,
        version: Optional[str] = "draft-07"
    ) -> None:
        
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
        return self._schema

    @classmethod
    def load_from_file(cls, file_path: Union[str, Path]) -> 'Schema':
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
        with open(file_path, 'w') as schema_file:
            json.dump(self._schema, schema_file, indent=4)

    def _get_version(self, schema_link: str) -> str:
        SCHEMA_VERSION_INDEX = -2
        schema_version = schema_link.split('/')[SCHEMA_VERSION_INDEX]
        return schema_version


class Serializer:
    @classmethod
    def serialize(
        cls,
        obj: object,
        schema_file_path: Optional[Union[str, Path]] = None
    ) -> Dict[str, Any]:
        
        seria = {}
        if schema_file_path is not None:
            seria["$schema"] = schema_file_path
        
        object_items = obj.__dict__.items()
        for field_name, field_value in object_items:
            if cls.__is_array(field_value):
                seria[field_name] = [cls.serialize(item) for item in field_value]
            elif cls.__is_object(field_value):
                seria[field_name] = cls.serialize(field_value)
            else:
                seria[field_name] = field_value

        if schema_file_path is not None:
            cls.validate(seria, schema_file_path)
        
        return seria

    @classmethod
    def deserialize(
        cls,
        seria: Union[Dict[str, Any], RootTree],
        seria_class: Type,
        seria_fields_types: Optional[Dict[str, Union[Type, Field]]] = None
    ) -> object:
        
        seria.pop("$schema", None)

        if seria_fields_types is not None:
            seria_fields_types = Field.wrap_all_types(seria_fields_types)

        parameters = {}
        for key, value in seria.items():
            if cls.__is_dict(value) or cls.__is_array(value):
                field = seria_fields_types[key]

            if cls.__is_dict(value):
                parameters[key] = cls.deserialize(value, field.type, field.types)
            elif cls.__is_array(value):
                array_item_type = cls.__extract_type(field.type)
                parameters[key] = [
                    cls.deserialize(
                        item,
                        array_item_type,
                        field.types
                    ) for item in value]
            else:
                parameters[key] = value

        return seria_class(**parameters)
    
    @classmethod
    def __extract_type(cls, field_type: Type) -> Type:
        if hasattr(field_type, '__origin__'):
            return get_args(field_type)[0]
        raise TypeError(f"{field_type} not supported.")

    @classmethod
    def __is_array(cls, value: Any) -> bool:
        return isinstance(value, (list, tuple))
    
    @classmethod
    def __is_object(cls, value: Any) -> bool:
        return hasattr(value, "__dict__")
    
    @classmethod
    def __is_dict(cls, value: Any) -> bool:
        return isinstance(value, dict)
    
    @classmethod
    def validate(
        cls,
        seria: Dict[str, Any],
        schema_file_path: Union[str, Path]
    ) -> None:
        
        with open(schema_file_path, 'r') as file:
            schema = json.load(file)

        Validator.check_schema(schema)
        jsonschema.validate(seria, schema)