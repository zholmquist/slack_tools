# import json
# from abc import ABCMeta
# from dataclasses import asdict, dataclass, field, is_dataclass
# from datetime import datetime
# from typing import Any, Literal


# class ModelMetaclass(ABCMeta):
#     def __new__(mcls, name, bases, namespace, block_type: str | None = None, **kwargs):
#         if block_type is not None:
#             annotations: dict[str, Any] = namespace.get('__annotations__', {})

#             if 'type' not in annotations:
#                 annotations['type'] = str
#             namespace['__annotations__'] = annotations

#             if 'type' not in namespace:
#                 namespace['type'] = block_type

#         return super().__new__(mcls, name, bases, namespace, **kwargs)


# class Base:
#     """Base dataclass for models."""

#     field_validators: dict | None = field(default=None, repr=False, init=False)

#     def to_dict(self) -> dict:
#         """Return dictionary representation."""
#         if is_dataclass(self):
#             return asdict(self)
#         elif isinstance(self, dict):
#             return self
#         else:
#             raise ValueError(f'Invalid type: {type(self)}')

#     def to_json(self) -> str:
#         """Return JSON string representation."""
#         return json.dumps(self.to_dict())

#     def __rich__(self):
#         return self


# @dataclass
# class BaseObject(Base):
#     """Base class for objects."""

#     pass


# @dataclass
# class BaseBlock(Base, metaclass=ModelMetaclass):
#     """Base class for blocks."""

#     pass


# @dataclass
# class BaseElement(Base, metaclass=ModelMetaclass):
#     """Base class for elements."""

#     pass


# class RichElement(BaseElement):
#     """Base class for rich elements."""

#     pass


# class InteractiveElement(BaseElement):
#     """Base class for interactive elements."""

#     pass


# # Types
# BlockSchema = dict[str, Any]
# BlockKitSchema = dict[str, BlockSchema]

# BlockJson = str
# BlockKitJson = str

# AnyDateType = str | int | datetime

# # Slack Types
# ButtonStyle = Literal['primary', 'danger']
# KeyboardEvents = Literal['on_character_entered', 'on_enter_pressed']
# ConversationTypes = Literal['im', 'mpim', 'private', 'public']
