# (c) KiryxaTech, 2024. Apache License 2.0. See the LICENSE file.

"""
The core classes for OOJ library.

**Method of application:**
```python
from ooj import JsonFile
from ooj.core_classes import *

data = Tree(
    Entry("name", "Alice"),
    Entry("age", "30"),
    Tree("passport",
        Entry("seria", "64 92"),
        Entry("number", "391049")
    )
)

file = JsonFile("test.json")
file.write(data)

data = file.read()
print(data) # Output: {"name": "Alice", "age": 30, "passport": {"seria": "64 92", "number": 391049}}
```
"""

from .entity import Entity
from .entry import Entry
from .tree import Tree

__all__ = ["Entity", "Entry", "Tree"]