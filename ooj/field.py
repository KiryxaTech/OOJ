from typing import Dict, Type, Optional, Union

class Field:
    """
    A class to represent a field in a data structure, encapsulating its type 
    and any nested types for deserialization purposes.

    Attributes:
        type_ (Type): The type of the field.
        types (Optional[Dict[str, Union[Type, Field]]]): A dictionary of nested 
            field types, if any.
    """

    def __init__(self, type_: Type, types: Optional[Dict[str, Union[Type, 'Field']]] = None):
        """
        Initializes a Field instance.

        Args:
            type_ (Type): The type of the field.
            types (Optional[Dict[str, Union[Type, 'Field']]]): A dictionary of nested 
                field types (default is None).
        """

        if not isinstance(types, dict) and not types is None:
            raise TypeError(f"The {types} is not a dictionary.")

        self.type = type_
        self.types = types

    @classmethod
    def wrap_type(cls, type_: Union[Type, 'Field']) -> 'Field':
        """
        Wraps the given type in a Field instance if it is not already wrapped.

        Args:
            type_ (Union[Type, 'Field']): The type to be wrapped.

        Returns:
            Field: A Field instance wrapping the given type.
        """
        if isinstance(type_, Field):
            return type_
        return Field(type_)

    @classmethod
    def wrap_all_types(cls, types: Dict[str, Union[Type, 'Field']]) -> Dict[str, 'Field']:
        """
        Wraps all types in the provided dictionary in Field instances.

        Args:
            types (Dict[str, Union[Type, 'Field']]): A dictionary of types to be wrapped.

        Returns:
            Dict[str, Field]: A dictionary with types wrapped in Field instances.
        """
        wrapped_types = {}
        for key, type_ in types.items():
            wrapped_types[key] = cls.wrap_type(type_)

        return wrapped_types