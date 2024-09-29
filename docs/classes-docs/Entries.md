### Documentation for `JsonEntity`, `Entry`, `BaseTree`, `RootTree`, `Tree`, and `TreeConverter` Classes

#### Overview
This module defines a framework for representing and manipulating JSON-like data structures using a tree-based approach. The key components include abstract base classes and concrete implementations that handle entries and tree structures, along with a converter for transforming dictionaries into these structures.

#### Class Descriptions

##### 1. `JsonEntity` (Abstract Base Class)
- **Purpose**: Defines the interface for JSON entities, requiring implementation of the `to_dict` method.
- **Methods**:
  - **`__str__()`**: Returns a string representation of the entity by converting it to a dictionary.
  - **`__eq__(value: Union[Dict[str, Any], 'JsonEntity'])`**: Compares the entity to another value for equality.
  - **`__ne__(value: Union[Dict[str, Any], 'JsonEntity'])`**: Compares the entity to another value for inequality.
  - **`to_dict() -> Dict`**: Abstract method that must be implemented in subclasses to convert the entity to a dictionary.

---

##### 2. `Entry` (Concrete Class)
- **Purpose**: Represents a key-value pair in the JSON structure.
- **Attributes**:
  - **`key`** (`str`): The key of the entry.
  - **`value`** (`Any`): The value associated with the key.
- **Methods**:
  - **`__str__()`**: Returns the dictionary representation of the entry.
  - **`__iter__()`**: Returns an iterator over the entry's key-value pair.
  - **`to_dict()`**: Converts the entry to a dictionary.

---

##### 3. `BaseTree` (Concrete Class)
- **Purpose**: Represents a tree structure that can contain both entries and subtrees.
- **Attributes**:
  - **`tree`** (`List[Union[Entry, 'BaseTree']]`): List of entries and subtrees.
- **Methods**:
  - **`__str__()`**: Returns the dictionary representation of the tree.
  - **`add(entry: Union[Entry, 'BaseTree'])`**: Adds an entry or subtree to the tree.
  - **`remove(key: str)`**: Removes an entry with the specified key from the tree.
  - **`to_dict()`**: Converts the tree to a dictionary, recursively processing entries and subtrees.

---

##### 4. `RootTree` (Concrete Class)
- **Purpose**: Represents the root of a tree structure, inheriting from `BaseTree`.
- **Methods**:
  - Inherits all methods from `BaseTree`.

---

##### 5. `Tree` (Concrete Class)
- **Purpose**: Represents a subtree with a specific key.
- **Attributes**:
  - **`key`** (`str`): The key associated with this subtree.
- **Methods**:
  - Inherits all methods from `BaseTree`.

---

##### 6. `TreeConverter` (Utility Class)
- **Purpose**: Provides methods to convert JSON-like dictionaries into tree structures.
- **Methods**:
  - **`to_root_tree(json_data: dict) -> RootTree`**: Converts a flat dictionary into a `RootTree`.
  - **`to_tree(key: str, json_data: dict) -> Tree`**: Converts a dictionary into a `Tree` structure based on the provided key.
  - **`to_dict(json_object: Union[Entry, Tree, RootTree]) -> Dict`**: Converts a `JsonEntity` (entry or tree) back into a dictionary.

#### Usage Examples

##### Example of Creating and Using Entries
```python
entry = Entry("name", "John Doe")
print(entry)  # Output: {'name': 'John Doe'}
```

##### Example of Creating a Tree Structure
```python
root_tree = RootTree()
root_tree.add(Entry("age", 30))
sub_tree = Tree("address")
sub_tree.add(Entry("city", "New York"))
sub_tree.add(Entry("zip", "10001"))
root_tree.add(sub_tree)

print(root_tree.to_dict())
# Output: {'age': 30, 'address': {'city': 'New York', 'zip': '10001'}}
```

##### Example of Converting JSON Data to a Tree
```python
json_data = {
    "name": "John Doe",
    "details": {
        "age": 30,
        "address": {
            "city": "New York",
            "zip": "10001"
        }
    }
}

root_tree = TreeConverter.to_root_tree(json_data)
print(root_tree.to_dict())
# Output: {'name': 'John Doe', 'details': {'age': 30, 'address': {'city': 'New York', 'zip': '10001'}}}
```