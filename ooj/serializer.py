# (c) KiryxaTech, 2024. Apache License 2.0

import json
from pathlib import Path
from typing import Any, Dict, List, Type, Optional, Union, get_args

import jsonschema
import jsonschema.exceptions
from jsonschema.protocols import Validator

from .entities import RootTree
from .exceptions.exceptions import SchemaException, ValidationException
from .field import Field


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