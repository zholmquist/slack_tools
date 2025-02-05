import json
from abc import ABCMeta
from dataclasses import asdict, field, is_dataclass
from typing import Any, Literal


class BlockTypeMetaclass(ABCMeta):
    def __new__(mcls, name, bases, namespace, block_type: str | None = None, **kwargs):
        if block_type is not None:
            annotations: dict[str, Any] = namespace.get('__annotations__', {})

            if 'type' not in annotations:
                annotations['type'] = str
            namespace['__annotations__'] = annotations

            if 'type' not in namespace:
                namespace['type'] = block_type

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


class ObjectSchema(BaseSchema, metaclass=BlockTypeMetaclass):
    """Base class for objects."""

    pass


class BlockSchema(BaseSchema, metaclass=BlockTypeMetaclass):
    """Base class for blocks."""

    pass


class ElementSchema(BaseSchema, metaclass=BlockTypeMetaclass):
    """Base class for elements."""

    pass


class InteractiveElementSchema(ElementSchema):
    """Base class for interactive elements."""

    pass


class RichElementSchema(ElementSchema):
    """Base class for rich elements."""

    pass


# Slack Types
ButtonStyle = Literal['primary', 'danger']
ListStyle = Literal['ordered', 'bullet']
KeyboardEvent = Literal['on_character_entered', 'on_enter_pressed']
ConversationType = Literal['im', 'mpim', 'private', 'public']
