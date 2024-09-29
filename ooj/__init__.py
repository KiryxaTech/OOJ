"""
:authors: KiryxaTech
:license Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2024 KiryxaTech
"""


READ_MODE = 'r'
WRITE_MODE = 'w'


from .base import JsonBase
from .file import JsonFile
from .objets import Entry, RootTree, Tree, JsonObject
from .serializer import Serializer
from .exceptions.exceptions import (NotSerializableException,
                                    CyclicFieldError)