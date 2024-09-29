# (c) KiryxaTech, 2024. Apache License 2.0

import json
from pathlib import Path
from typing import Any, Dict, List, Type, Optional, Union, get_args, get_origin

import jsonschema
import jsonschema.exceptions
from jsonschema.protocols import Validator

from .entities import RootTree
from .exceptions.exceptions import SchemaException, ValidationException


class Field:
    """
    A class to represent a field in a data structure, encapsulating its type 
    and any nested types for deserialization purposes.

    Attributes:
        type_ (Type): The type of the field.
        types (Optional[Dict[str, Union[Type, Field]]]): A dictionary of nested 
            field types, if any.
    """

    def __init__(self, type_: Type, types: Optional[Dict[str, Union[Type, 'Field']]] = None):
        """
        Initializes a Field instance.

        Args:
            type_ (Type): The type of the field.
            types (Optional[Dict[str, Union[Type, 'Field']]]): A dictionary of nested 
                field types (default is None).
        """

        if not isinstance(types, dict) and not types is None:
            raise TypeError(f"The {types} is not a dictionary.")

        self.type = type_
        self.types = types

    @classmethod
    def wrap_type(cls, type_: Union[Type, 'Field']) -> 'Field':
        """
        Wraps the given type in a Field instance if it is not already wrapped.

        Args:
            type_ (Union[Type, 'Field']): The type to be wrapped.

        Returns:
            Field: A Field instance wrapping the given type.
        """
        if isinstance(type_, Field):
            return type_
        return Field(type_)

    @classmethod
    def wrap_all_types(cls, types: Dict[str, Union[Type, 'Field']]) -> Dict[str, 'Field']:
        """
        Wraps all types in the provided dictionary in Field instances.

        Args:
            types (Dict[str, Union[Type, 'Field']]): A dictionary of types to be wrapped.

        Returns:
            Dict[str, Field]: A dictionary with types wrapped in Field instances.
        """
        wrapped_types = {}
        for key, type_ in types.items():
            wrapped_types[key] = cls.wrap_type(type_)

        return wrapped_types


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


class Serializer:
    """
    A class for serializing and deserializing objects to and from JSON format.

    Methods:
        serialize(obj: object, schema_file_path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
            Serializes an object into a JSON-compatible dictionary format.
        
        deserialize(seria: Union[Dict[str, Any], RootTree], seria_class: Type, 
                    seria_fields_types: Optional[Dict[str, Union[Type, Field]]] = None) -> object:
            Deserializes a JSON-compatible dictionary back into an object of the specified class.
        
        validate(seria: Dict[str, Any], schema_file_path: Union[str, Path]) -> None:
            Validates the serialized data against a specified JSON schema.

    Usage Examples:
        Example of serialization:
        ```python
        from ooj import Serializer

        class ExampleClass:
            def __init__(self, name: str, age: int):
                self.name = name
                self.age = age

        example_object = ExampleClass(name="Alice", age=30)
        serialized_data = Serializer.serialize(example_object)
        print(serialized_data)
        ```

        Example of deserialization:
        ```python
        from ooj import Serializer

        serialized_data = {"name": "Alice", "age": 30}
        
        deserialized_object = Serializer.deserialize(serialized_data, ExampleClass)
        print(deserialized_object.name)  # Output: Alice
        print(deserialized_object.age)   # Output: 30
        ```

    """

    @classmethod
    def serialize(
        cls,
        object_: object,
        schema_file_path: Optional[Union[str, Path]] = None
    ) -> Dict[str, Any]:
        """Serializes an object into a JSON-compatible dictionary format.

        Args:
            obj (object): The object to serialize.
            schema_file_path (Optional[Union[str, Path]]): Optional path to the JSON schema file to validate against.

        Returns:
            Dict[str, Any]: A dictionary representing the serialized object.
        """
        
        seria = {}
        if schema_file_path is not None:
            seria["$schema"] = schema_file_path
        
        object_items = object_.__dict__.items()
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
        seria_type: Type,
        seria_fields_types: Optional[Dict[str, Union[Type, Field]]] = None
    ) -> object:
        """Deserializes a JSON-compatible dictionary back into an object of the specified class.

        Args:
            seria (Union[Dict[str, Any], RootTree]): The serialized dictionary or RootTree to deserialize.
            seria_type (Type): The class of the object to create.
            seria_fields_types (Optional[Dict[str, Union[Type, Field]]]): Optional mapping of field names to types.

        Returns:
            object: An instance of the specified class with the deserialized data.
        """
        
        seria.pop("$schema", None)

        if seria_fields_types is not None:
            seria_fields_types = Field.wrap_all_types(seria_fields_types)

        parameters = {}
        for key, value in seria.items():
            field = cls.__get_field_type(key, value, seria_fields_types, seria_type)

            if cls.__is_dict(value):
                parameters[key] = cls.deserialize_dict(value, field)
            elif cls.__is_array(value):
                parameters[key] = cls.deserialize_array(value, field)
            else:
                parameters[key] = value

        return seria_type(**parameters)

    @classmethod
    def __get_field_type(cls, key: str, value: Any, seria_fields_types: Optional[Dict[str, Union[Type, Field]]], seria_type: Type) -> Type:
        """Gets the field type based on the serialized value and class annotations."""
        if seria_fields_types is not None:
            field = seria_fields_types.get(key, Field(None))
        else:
            field = Field(None)

        field_type = field.type

        if cls.__has_annotations(seria_type):
            field_type = seria_type.__init__.__annotations__.get(key, field_type)

        return field_type

    @classmethod
    def deserialize_dict(cls, value: Dict[str, Any], field: Type) -> object:
        """Deserializes a dictionary using the specified field type."""
        if field is None:
            return value
        return cls.deserialize(value, field, field.__init__.__annotations__ if cls.__has_annotations(field) else {})

    @classmethod
    def deserialize_array(cls, value: List[Any], field: Type) -> List[Any]:
        """Deserializes an array using the specified field type."""
        item_type = cls.__extract_type(field)
        return [
            cls.deserialize(item, item_type, field.__init__.__annotations__ if cls.__has_annotations(field) else {})
            for item in value if item is not None
        ]
    
    @classmethod
    def validate(
        cls,
        seria: Dict[str, Any],
        schema_file_path: Union[str, Path]
    ) -> None:
        """Validates the serialized data against a specified JSON schema.

        Args:
            seria (Dict[str, Any]): The serialized data to validate.
            schema_file_path (Union[str, Path]): The path to the JSON schema file.
        
        Raises:
            jsonschema.exceptions.ValidationError: If the serialized data does not conform to the schema.
        """
        with open(schema_file_path, 'r') as file:
            schema = json.load(file)

        try:
            Validator.check_schema(schema)
            jsonschema.validate(seria, schema)
        except jsonschema.exceptions.SchemaError as e:
            raise SchemaException(e)
        except jsonschema.exceptions.ValidationError as e:
            raise ValidationException(e)

    @staticmethod
    def __has_annotations(seria_type):
        return hasattr(seria_type.__init__, "__annotations__")

    @staticmethod
    def __extract_type(field_type: Type) -> Type:
        """Extracts the type from a generic type.

        Args:
            field_type (Type): The type from which to extract the generic type.

        Returns:
            Type: The extracted type.

        Raises:
            TypeError: If the field type is not supported.
        """
        if hasattr(field_type, '__origin__'):
            return get_args(field_type)[0]
        raise TypeError(f"{field_type} not supported.")

    @staticmethod
    def __is_array(value: Any) -> bool:
        """Checks if the given value is an array (list or tuple).

        Args:
            value (Any): The value to check.

        Returns:
            bool: True if the value is an array; otherwise, False.
        """
        return isinstance(value, (list, tuple))
    
    @staticmethod
    def __is_object(value: Any) -> bool:
        """Checks if the given value is an object.

        Args:
            value (Any): The value to check.

        Returns:
            bool: True if the value has a __dict__ attribute; otherwise, False.
        """
        return hasattr(value, "__dict__")
    
    @staticmethod
    def __is_dict(value: Any) -> bool:
        """Checks if the given value is a dictionary.

        Args:
            value (Any): The value to check.

        Returns:
            bool: True if the value is a dictionary; otherwise, False.
        """
        return isinstance(value, dict)