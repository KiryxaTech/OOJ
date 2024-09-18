class NotSerializableException(Exception):
    def __init__(self):
        super().__init__('Cannot serialize or deserialize object')


class CyclicFieldError(Exception):
    def __init__(self):
        super().__init__('Cyclic field detected')

class FileExtensionException(Exception):
    def __init__(self, message: str = None):
        super().__init__(message=message)