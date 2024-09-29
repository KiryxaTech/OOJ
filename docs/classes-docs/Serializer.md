### Documentation for `Serializer` Class

#### Description
The `Serializer` class is designed for serializing and deserializing objects to and from JSON format. It provides methods to convert Python objects into JSON-compatible dictionary formats and to reconstruct objects from those formats. Additionally, it includes validation against JSON schemas to ensure the integrity of serialized data.

#### Methods
- **`serialize(obj: object, schema_file_path: Optional[Union[str, Path]] = None) -> Dict[str, Any]`**
    - Serializes an object into a JSON-compatible dictionary format.
  
- **`deserialize(seria: Union[Dict[str, Any], RootTree], seria_type: Type, seria_fields_types: Optional[Dict[str, Union[Type, Field]]] = None) -> object`**
    - Deserializes a JSON-compatible dictionary back into an object of the specified class.
  
- **`validate(seria: Dict[str, Any], schema_file_path: Union[str, Path]) -> None`**
    - Validates the serialized data against a specified JSON schema.

#### Usage Examples

##### Example of Serialization
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

##### Example of Deserialization
```python
from ooj import Serializer

serialized_data = {"name": "Alice", "age": 30}

deserialized_object = Serializer.deserialize(serialized_data, ExampleClass)
print(deserialized_object.name)  # Output: Alice
print(deserialized_object.age)   # Output: 30
```

#### Parameters
- **`obj`** (`object`): The object to serialize.
- **`schema_file_path`** (`Optional[Union[str, Path]]`): Optional path to the JSON schema file for validation during serialization.
- **`seria`** (`Union[Dict[str, Any], RootTree]`): The serialized dictionary or `RootTree` to deserialize.
- **`seria_type`** (`Type`): The class of the object to create during deserialization.
- **`seria_fields_types`** (`Optional[Dict[str, Union[Type, Field]]]`): Optional mapping of field names to types for deserialization.
  
#### Return Values
- **`serialize`**: Returns a dictionary representing the serialized object.
- **`deserialize`**: Returns an instance of the specified class with the deserialized data.
- **`validate`**: Raises exceptions if the serialized data does not conform to the specified JSON schema.

#### Exceptions
- **`SchemaException`**: Raised when there is an error in the JSON schema.
- **`ValidationException`**: Raised when the serialized data fails validation against the schema.

#### Internal Methods
- **`__get_field_type(...)`**: Determines the field type based on the serialized value and class annotations.
- **`deserialize_dict(...)`**: Deserializes a dictionary using the specified field type.
- **`deserialize_array(...)`**: Deserializes an array using the specified field type.
- **`__has_annotations(...)`**: Checks if a class has annotations defined for its `__init__` method.
- **`__extract_type(...)`**: Extracts the type from a generic type.
- **`__is_array(...)`**: Checks if a given value is an array (list or tuple).
- **`__is_object(...)`**: Checks if a given value is an object.
- **`__is_dict(...)`**: Checks if a given value is a dictionary.