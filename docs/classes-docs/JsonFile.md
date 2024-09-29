### Documentation for `JsonFile` Class

#### Description
The `JsonFile` class simplifies working with JSON files by providing methods for reading, writing, and deleting data, as well as handling tree structures (`RootTree`). An internal buffer allows faster access to the data.

#### Constructor Arguments
- **`fp`** (`Union[str, Path]`): The path to the JSON file.
- **`encoding`** (`str`, default: `"utf-8"`): Encoding used for reading and writing files.
- **`indent`** (`int`, default: `4`): Indentation used for formatting JSON.
- **`ignore_errors`** (`List[Exception]`, default: `None`): A list of exceptions to be ignored during read/write operations.

#### Example Usage

```python
from ooj import JsonFile

# Create a new JsonFile object
json_file = JsonFile("data.json")

# Write a dictionary to a JSON file
data = {"name": "John", "age": 30}
json_file.write(data)

# Read data from the file
read_data = json_file.read()
print(read_data)  # Output: {'name': 'John', 'age': 30}

# Set a new value at a specified key
json_file.set_entry("address", {"city": "New York", "zip": "10001"})

# Get a value by key
address = json_file.get_entry("address")
print(address)  # Output: {'city': 'New York', 'zip': '10001'}

# Delete an entry by key
json_file.del_entry("address")

# Check if the file exists
if json_file.exists:
    print("File exists.")
else:
    print("File not found.")
```

#### Methods

- **`create()`**: Creates the file if it doesn't exist.
- **`create_if_not_exists()`**: Creates the file only if it does not already exist.
- **`delete()`**: Deletes the file.
- **`clear()`**: Clears the content of the file.
- **`write(data: Union[Dict, RootTree])`**: Writes a dictionary to the file.
- **`read() -> Dict`**: Reads data from the file and returns it as a dictionary.
- **`read_tree() -> RootTree`**: Reads the data from the file and returns it as a `RootTree` object.
- **`set_entry(key_s: Union[List[str], str], value: Union[Any, Entry, RootTree])`**: Updates the value at the specified key path. If intermediate keys are missing, they are created.
- **`get_entry(key_s: Union[List[str], str]) -> Any`**: Returns the value at the specified key path.
- **`del_entry(key_s: Union[List[str], str])`**: Deletes an entry at the specified key path.
- **`update_buffer_from_file()`**: Updates the internal buffer by reading the current data from the file.
- **`exists`**: Property that returns `True` if the file exists.
- **`_handle_exception(e: Exception)`**: Handles exceptions during file operations. If the exception is listed in `ignore_errors`, it is ignored.
  
#### Exceptions
- **`FileExtensionException`**: Raised if the file does not have a `.json` extension.
- **`KeyError`**: Raised if a key is not found during `get_entry()` or `del_entry()`.
- **`TypeError`**: Raised when attempting to write an unsupported data type.