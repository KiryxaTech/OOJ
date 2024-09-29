### Documentation for `JsonURL` Class

#### Overview
The `JsonURL` class is designed to fetch JSON data from a specified URL and optionally save the data to a file. This class extends the functionality of the `JsonBase` class, handling URL validation, data loading, and file operations.

#### Class Description

##### `JsonURL`
- **Inherits**: `JsonBase`
- **Purpose**: To load JSON data from a URL and provide the option to save that data to a file.
  
##### Attributes:
- **`url`** (`str`): The URL to fetch JSON data from.
- **`output_file_path`** (`Optional[Union[Path, str]]`): The file path where the JSON data will be saved (if specified).
- **`encoding`** (`Optional[str]`): The encoding to use when saving the JSON file. Default is `"utf-8"`.
- **`indent`** (`Optional[int]`): The number of spaces for indentation when saving the JSON file. Default is `4`.
- **`ignore_exceptions_list`** (`Optional[List[Exception]]`): A list of exceptions that should be ignored during processing. Default is an empty list.

---

#### Methods

- **`__init__(url: str, output_file_path: Optional[Union[Path, str]] = None, encoding: Optional[str] = "utf-8", indent: Optional[int] = 4, ignore_exceptions_list: Optional[List[Exception]] = None)`**
  - **Purpose**: Initializes a `JsonURL` instance and validates the URL.
  - **Args**:
    - `url`: The URL to fetch JSON data from.
    - `output_file_path`: The optional file path for saving the JSON data.
    - `encoding`: The file encoding for saving the JSON data.
    - `indent`: The indentation level for the JSON output.
    - `ignore_exceptions_list`: A list of exceptions to ignore.

- **`load_from_url() -> Dict`**
  - **Purpose**: Fetches JSON data from the specified URL.
  - **Returns**: The loaded JSON data as a dictionary.
  - **Raises**: Raises an exception if an error occurs and it is not in the ignore exceptions list.

- **`_dump_to_file(data: Dict) -> None`**
  - **Purpose**: Saves the provided JSON data to a file.
  - **Args**: 
    - `data`: The JSON data to be saved.

- **`to_json_file() -> JsonFile`**
  - **Purpose**: Converts the loaded JSON data to a `JsonFile` instance.
  - **Returns**: An instance of `JsonFile` containing the JSON data.

- **`_validate_url() -> None`**
  - **Purpose**: Validates the specified URL format.
  - **Raises**: 
    - `ValueError`: If the URL is invalid.

---

#### Usage Examples

##### Example of Creating a JsonURL Instance
```python
json_url = JsonURL("https://api.example.com/data.json", output_file_path="data.json")
```

##### Example of Loading JSON Data
```python
data = json_url.load_from_url()
print(data)  # Output: Loaded JSON data as a dictionary
```

##### Example of Saving JSON Data to a File
```python
json_url._dump_to_file(data)  # Saves the loaded JSON data to 'data.json'
```

##### Example of Converting to JsonFile
```python
json_file = json_url.to_json_file()
print(json_file)  # Output: JsonFile instance with the loaded JSON data
```

---

#### Error Handling
- If an invalid URL is provided, a `ValueError` will be raised.
- Any exceptions encountered during data loading can be ignored if specified in the `ignore_exceptions_list`.