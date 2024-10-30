<div align="center">
    <picture>
        <source media="(prefers-color-scheme: dark)" srcset="./docs/project-logo/OOJ.png">
        <img src="./docs/project-logo/OOJ.png">
    </picture>

![PyPI Version](https://img.shields.io/pypi/v/ooj)
![Month Downloads](https://static.pepy.tech/badge/ooj/month)
![Total Downloads](https://static.pepy.tech/badge/ooj)
![Project License](https://img.shields.io/badge/license-Apache2.0-e6b064)
</div>


`Object-Oriented JSON (OOJ)` is a universal library for working with JSON in Python, providing simplicity and convenience in serializing and deserializing complex objects.

## Table of Contents

- [Installation](#installation)
- [Core Classes](#core-classes)
- [Usage Example](#usage-example)
- [Support for Nested Types](#support-for-nested-types)
- [License](#license)

## Installation

Install the library via `pip`:

```bash
pip install ooj
```

## Core Classes

### `Entry`

A class representing a key-value pair in JSON. It implements methods for serialization to a dictionary and comparison.

### `RootTree` and `Tree`

Classes extending `BaseTree` that provide structuring for nested objects.

### `TreeConverter`

A class for converting JSON data into `RootTree` and `Tree` structures.

## Usage Example

```python
from ooj import TreeConverter

json_data = {
    "name": "Alice",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "Anytown"
    }
}

root_tree = TreeConverter.to_root_tree(json_data)
print(root_tree)
```

## Write and Read
```python
from ooj import JsonFile

file = JsonFile("test.json")

# Write to file.
file.write({"name": "Alice"})

# Read from file.
data = file.read()
print(data) # Output: {"name": "Alice"}
```

## License

This project is licensed under the Apache 2.0 License. See the `LICENSE` file for more information.