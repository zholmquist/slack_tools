from dataclasses import field
from typing import Callable, Self

from slack_tools.actions.schemas import ActionCallback


class CallableElementMixin:
    """Mixin for elements that can be called."""

    _callback: Callable | None = field(default=None, repr=False, init=False)

    def get_action(self) -> ActionCallback | None:
        if self._callback:
            return ActionCallback(
                action_id=self.action_id,
                callback=self._callback,
            )
        return None

    def action(self, callback: Callable) -> Self:
        self._callback = callback
        return self
