# (c) KiryxaTech, 2024. Apache License 2.0. See the LICENSE file.

"""
Exceptions for OOJ library.

**Includes:**
- SchemaException: invalid schema.
- ValidationException: the object does not match the schema
- FileExtensionException: the file extension is not ".json".
"""

from .exceptions import (
    SchemaException,
    ValidationException,
    FileExtensionException
)

__all__ = [
    "SchemaException",
    "ValidationException",
    "FileExtensionException"
]