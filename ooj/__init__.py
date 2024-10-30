# (c) KiryxaTech, 2024. Apache License 2.0. See the LICENSE file.

"""
Object-Oriented JSON is a module for working with JSON files and objects.

**Core Classes:**
```python
from ooj.core_classes import RootTree, Tree, Entry

tree = RootTree(
    Entry("key", "value"),
    Tree("tree"
        Entry("key", "value"),
        ...
    )
)
print(tree.to_dict()) # Output: {"key": "value", "tree": {"key": "value"}}
```

Write and Read the file:**
```python
from ooj import JsonFile

file = JsonFile("test.json")
file.write({"key": "value"})

data = file.read()
print(data) # Output: {"key": "value"}
```

**Get and set key:**
```python
from ooj import JsonFile

file = JsonFile("test.json")

data = {
   "key": "value",
   "tree": {
        "key": "nested_value"
    }
}
file.write(data)

file.set_entry(["tree", "key"], "changed_nested_value")

entry = file.get_entry(["tree", "key"])
print(entry) # Output: cnanged_nested_value
```

**Serilize and deserialize:**
```python
from ooj import Serializer

class Person:
    # Annotations is required for deserialization!
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

person = Person("Alice", 30)

# Serialization
data = Serializer.serialize(person)
print(data) # Output: {"name": "Alice", "age": 30}

# Deserialization
person = Serializer.deserialize(data)
print(person) # Output: <__main__.Person object at 0x000001F51EDFD280>
```

**Schema creating:**
```python
from ooj import Schema

schema = Schema(
    title="Test schema",
    type_="object",
    properties={
        "name": str,
        "age": int
    },
    required=["name", "age"],
    version="draft-07"
)
"""

from . import core_classes, exceptions
from .base import JsonBase
from .field import Field
from .file import JsonFile
from .schema import Schema
from .serializer import Serializer
from .url import JsonURL

__all__ = [
    "core_classes",
    "exceptions",
    "Field",
    "JsonBase",
    "JsonFile",
    "JsonURL",
    "Schema",
    "Serializer",
]