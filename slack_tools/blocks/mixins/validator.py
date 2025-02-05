from typing import TypeVar, Union, get_args, get_origin

T = TypeVar('T')


class TypeValidatorMixin:
    """Mixin to validate field types in block schemas."""

    def validate_field_type(self, field_name: str) -> None:
        """Validate that a field's value matches its type annotation.

        Args:
            field_name: Name of the field to validate

        Raises:
            ValueError: If field value doesn't match the type annotation
            AttributeError: If field doesn't exist
        """
        value = getattr(self, field_name)
        if value is None:
            return

        field_type = self.__annotations__[field_name]
        origin_type = get_origin(field_type)

        # Handle Optional/Union types
        if origin_type is Union:
            allowed_types = get_args(field_type)
            # Filter out NoneType for Optional fields
            allowed_types = tuple(t for t in allowed_types if t != type(None))
            if not isinstance(value, allowed_types):
                type_names = ' or '.join(t.__name__ for t in allowed_types)
                raise ValueError(f'{field_name} must be an instance of {type_names}')
            return

        # Handle list types
        if origin_type is list:
            element_type = get_args(field_type)[0]
            element_origin = get_origin(element_type)

            # Handle Union types within lists
            if element_origin is Union:
                allowed_types = get_args(element_type)
                if not all(isinstance(elem, allowed_types) for elem in value):
                    type_names = ' or '.join(t.__name__ for t in allowed_types)
                    raise ValueError(
                        f'All elements in {field_name} must be instances of {type_names}'
                    )
            else:
                if not all(isinstance(elem, element_type) for elem in value):
                    raise ValueError(
                        f'All elements in {field_name} must be instances of {element_type.__name__}'
                    )
            return

        # Handle single value types (non-Union)
        if not isinstance(value, field_type):
            # For non-Union types, we can use __name__ directly
            type_name = getattr(field_type, '__name__', str(field_type))
            raise ValueError(f'{field_name} must be an instance of {type_name}')
