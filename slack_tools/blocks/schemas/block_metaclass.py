from abc import ABCMeta
from dataclasses import Field
from typing import Any, Type

from slack_tools.exceptions import LengthValidationError


class FieldValidator:
    """Handles validation of field constraints like min/max length."""

    @staticmethod
    def validate_length(field_name: str, value: Any, field: Field):
        """Validates that the value meets min/max length constraints."""
        if value is None or value == field.default:
            return  # Skip validation for None or default values

        metadata = field.metadata
        min_length = metadata.get('min_length')
        max_length = metadata.get('max_length')

        if min_length is None and max_length is None:
            return  # No length constraints

        value_length = (
            len(value)
            if isinstance(value, (str, list, tuple, dict))
            else len(str(value))
        )

        if (min_length and value_length < min_length) or (
            max_length and value_length > max_length
        ):
            raise LengthValidationError(
                field_name, value_length, min_length, max_length
            )


class BlockMetaclass(ABCMeta):
    """Metaclass for Block Kit schemas.

    - Automatically sets the `type` attribute for blocks.
    - Runs validation on fields using standalone validators.
    """

    def __new__(
        mcls: Type['BlockMetaclass'],
        name: str,
        bases: tuple,
        namespace: dict[str, Any],
        block_type: str | None = None,
        **kwargs,
    ):
        """Creates a new class with type and validation logic."""
        if block_type is not None:
            mcls.set_block_type(namespace, block_type)
            fields = mcls.extract_fields(namespace)
            mcls.inject_post_init(namespace, fields)

        return super().__new__(mcls, name, bases, namespace, **kwargs)

    @staticmethod
    def set_block_type(namespace: dict[str, Any], block_type: str):
        """Ensures the `type` annotation and default value are set in the class."""
        annotations = namespace.setdefault('__annotations__', {})

        if 'type' not in annotations:
            annotations['type'] = str

        if 'type' not in namespace:
            namespace['type'] = block_type

    @staticmethod
    def extract_fields(namespace: dict[str, Any]) -> dict[str, Field]:
        """Extracts fields that have length constraints in their metadata."""
        return {
            field_name: field_value
            for field_name, field_value in namespace.items()
            if isinstance(field_value, Field)
            and field_value.metadata
            and (
                'min_length' in field_value.metadata
                or 'max_length' in field_value.metadata
            )
        }

    @staticmethod
    def inject_post_init(namespace: dict[str, Any], fields: dict[str, Field]):
        """Wraps `__post_init__` to perform field validation."""
        original_post_init = namespace.get('__post_init__')

        def __post_init__(self):
            """Runs validation logic after object initialization."""
            if original_post_init:
                original_post_init(self)

            for field_name, field in fields.items():
                value = getattr(self, field_name, None)
                FieldValidator.validate_length(field_name, value, field)

        namespace['__post_init__'] = __post_init__
