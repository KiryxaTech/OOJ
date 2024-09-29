# (c) KiryxaTech 2024. Apache License 2.0


class FileExtensionException(Exception):
    def __init__(self, message: str = None) -> None:
        super().__init__(message) or "The file extension is incorrect."


class SchemaException(Exception):
    def __init__(self, message: str = None) -> None:
        self.message = message or "Schema is invalid."
        super().__init__(message)


class ValidationException(Exception):
    def __init__(self, message: str = None) -> None:
        self.message = message or "The data does not match the schema."
        super().__init__(message)