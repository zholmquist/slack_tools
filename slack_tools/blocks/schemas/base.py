import json
from abc import ABCMeta
from dataclasses import asdict, field, is_dataclass
from typing import Any

from slack_tools.exceptions import LengthValidationError
from slack_tools.utils.dataclass_utils import Field


class BlockKitMetaclass(ABCMeta):
    def __new__(mcls, name, bases, namespace, block_type: str | None = None, **kwargs):
        if block_type is not None:
            annotations: dict[str, Any] = namespace.get('__annotations__', {})

            if 'type' not in annotations:
                annotations['type'] = str
            namespace['__annotations__'] = annotations

            if 'type' not in namespace:
                namespace['type'] = block_type

            # Get all Field instances and their names
            fields = {
                field_name: field_value
                for field_name, field_value in namespace.items()
                if isinstance(field_value, Field)
            }

            # Add validation to __post_init__ if it doesn't exist
            original_post_init = namespace.get('__post_init__')

            def __post_init__(self):
                # Call original __post_init__ if it exists
                if original_post_init:
                    original_post_init(self)

                # Validate length constraints for all fields
                for field_name, field in fields.items():
                    value = getattr(self, field_name)
                    default = getattr(field, 'default', None)
                    min_length = getattr(field, 'min_length', None)
                    max_length = getattr(field, 'max_length', None)

                    if value is not None and value != default:
                        if min_length is not None or max_length is not None:
                            value_length = (
                                len(value)
                                if isinstance(value, (str, list, tuple, dict))
                                else len(str(value))
                            )

                            if (min_length and value_length < min_length) or (
                                max_length and value_length > max_length
                            ):
                                raise LengthValidationError(
                                    field_name,
                                    value_length,
                                    min_length,
                                    max_length,
                                )

            namespace['__post_init__'] = __post_init__

        return super().__new__(mcls, name, bases, namespace, **kwargs)


class BaseSchema:
    """Base dataclass for models."""

    field_validators: dict | None = field(default=None, repr=False, init=False)

    def to_dict(self) -> dict:
        """Return dictionary representation."""
        if is_dataclass(self):
            return asdict(self)
        elif isinstance(self, dict):
            return self
        else:
            raise ValueError(f'Invalid type: {type(self)}')

    def to_json(self) -> str:
        """Return JSON string representation."""
        return json.dumps(self.to_dict())


class ObjectSchema(BaseSchema, metaclass=BlockKitMetaclass):
    """Base class for objects."""

    pass


class BlockSchema(BaseSchema, metaclass=BlockKitMetaclass):
    """Base class for blocks."""

    pass


class ElementSchema(BaseSchema, metaclass=BlockKitMetaclass):
    """Base class for elements."""

    pass


class InteractiveElementSchema(ElementSchema):
    """Base class for interactive elements."""

    pass


class RichElementSchema(ElementSchema):
    """Base class for rich elements."""

    pass


class RichBlockSchema(BlockSchema):
    """Base class for rich blocks."""

    pass
