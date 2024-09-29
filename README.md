<div align="center">
    <picture>
        <source media="(prefers-color-scheme: dark)" srcset="./docs/project-logo/OOJ.png">
        <img src="./docs/project-logo/OOJ.png">
    </picture>

![PyPI](https://img.shields.io/pypi/v/ooj)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ooj?color=green&label=downloads)
![Downloads last 6 month](https://static.pepy.tech/personalized-badge/ooj?period=total&units=international_system&left_color=grey&right_color=green&left_text=downloads%20last%206%20month)
![PyPI - License](https://img.shields.io/badge/license-Apache2.0-blue)
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

### `JsonEntity`

An abstract class representing the base for all JSON objects. It provides methods for converting objects to a dictionary and checking their equality.

### `Entry`

A class representing a key-value pair in JSON. It implements methods for serialization to a dictionary and comparison.

### `BaseTree`

A class representing a tree of JSON objects. It supports adding and removing elements and serializing to a dictionary.

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

## Support for Nested Types

The OOJ library supports deserializing complex nested types, allowing you to easily handle structures with arbitrary nesting. When serializing and deserializing, you can use annotations to specify data types, simplifying the work with custom objects and arrays.

Example:

```python
from ooj import Serializer

class Address(JsonEntity):
    def __init__(self, street: str, city: str):
        self.street = street
        self.city = city

    def to_dict(self):
        return {
            "street": self.street,
            "city": self.city
        }

class Person(JsonEntity):
    def __init__(self, name: str, age: int, address: Address):
        self.name = name
        self.age = age
        self.address = address

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "address": self.address.to_dict()
        }

address = Address("123 Main St", "Anytown")
person = Person("Alice", 30, address)
json_dict = person.to_dict()
print(json_dict)
```

## License

This project is licensed under the Apache 2.0 License. See the `LICENSE` file for more information.