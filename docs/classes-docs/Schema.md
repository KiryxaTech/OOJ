### Documentation for `Schema` Class

#### Description
The `Schema` class represents a JSON Schema, providing functionality to define, load, and save JSON schemas in a structured manner. It includes attributes for schema properties and methods to convert the schema to a dictionary format, load it from a file, and dump it to a file.

#### Attributes
- **`title`** (`str`): The title of the schema.
- **`type_`** (`Optional[str]`): The type of the schema. Defaults to "object".
- **`properties`** (`Optional[Dict[str, Any]]`): The properties of the schema.
- **`required`** (`Optional[List[str]]`): The required properties of the schema.
- **`version`** (`Optional[str]`): The version of the schema. Defaults to "draft-07".
- **`_schema`** (`Dict[str, Any]`): The internal representation of the JSON schema.

#### Methods
- **`__init__(title: str, type_: Optional[str] = "object", properties: Optional[Dict[str, Any]] = None, required: Optional[List[str]] = None, version: Optional[str] = "draft-07")`**
    - Initializes a `Schema` instance with the provided attributes.
  
- **`to_dict() -> Dict[str, Any]`**
    - Converts the schema to a dictionary format.

- **`load_from_file(file_path: Union[str, Path]) -> 'Schema'`**
    - Loads a schema from a JSON file and returns a `Schema` instance.
  
- **`dump_to_file(file_path: Union[str, Path]) -> None`**
    - Dumps the schema to a JSON file.

- **`_get_version(schema_link: str) -> str`**
    - Extracts the version from the schema link.

#### Usage Examples

##### Example of Creating a Schema
```python
from ooj import Schema

# Creating a new schema
schema = Schema(
    title="Example Schema",
    properties={"name": {"type": "string"}, "age": {"type": "integer"}},
    required=["name"]
)

schema_dict = schema.to_dict()
print(schema_dict)
```

##### Example of Loading a Schema from a File
```python
from ooj import Schema

# Load schema from a JSON file
loaded_schema = Schema.load_from_file("path/to/schema.json")
print(loaded_schema.to_dict())
```

##### Example of Dumping a Schema to a File
```python
from ooj import Schema

# Create a new schema and dump it to a file
schema = Schema(
    title="Example Schema",
    properties={"name": {"type": "string"}, "age": {"type": "integer"}},
    required=["name"]
)
schema.dump_to_file("path/to/output_schema.json")
```

#### Return Values
- **`to_dict`**: Returns the JSON schema as a dictionary.
- **`load_from_file`**: Returns a `Schema` instance representing the loaded schema.
- **`dump_to_file`**: Returns `None`.

#### Exceptions
- **`jsonschema.exceptions.SchemaError`**: Raised if the loaded schema does not conform to JSON schema standards.

#### Internal Methods
- **`_get_version(schema_link: str) -> str`**: Extracts the version from the schema link, returning the extracted version of the schema.