from typing import Generic, Self, TypeVar

from slack_tools.blocks.schemas.base import BaseSchema

T = TypeVar('T', bound=BaseSchema)


class CollectableElementMixin(Generic[T]):
    """Mixin to allow adding items via obj[item, item, item] syntax."""

    _collect_field: str = 'options'
    """Defines the field to collect items into."""

    def __getitem__(self: Self, items: T | tuple[T, ...] | list[T]) -> Self:
        """Add items to the designated collection field."""
        if isinstance(items, tuple):
            items = list(items)
        elif not isinstance(items, list):
            items = [items]
        return self.__class__(**{self._collect_field: items})
