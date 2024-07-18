# OOJ using guide

## Installation
You can install the `OOJ` library directly from PyPI:

### On Windows:
```bash
pip install ooj
```

### On Linux/MacOS:
```bash
pip3 install ooj
```

## Import
```python
import ooj
```

## Creating file
```python 
from ooj import JsonFile

file = JsonFile('your/path/to/file.json')
```

## Write
```python
data = {
    "a": {
        "b": 0
    },
    "c": "create release"
}

file.write(data)
```

## Read
```python
data = file.read()
```

## Add key
```python
file.set_value(keys, value)
```

## Remove key
```python
file.delete_key(keys)
```