import uuid
from typing import Callable, Self

from slack_tools.actions.schemas import ActionCallback


class ActionHandler:
    """Handles callback actions for a Slack app.

    TODO: Make it so we can save the callbacks if outstanding
    TODO: Add a cleanup method to delete callbacks that are no longer in use(?)
    """

    action_callbacks: dict[str, ActionCallback] = {}

    _instance = None

    def __new__(cls, *args, **kwargs) -> Self:
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def register(self, action_id: str, callback: Callable):
        self.action_callbacks[action_id] = ActionCallback(
            action_id=action_id, callback=callback
        )

    def get_callback(self, action_id: str) -> ActionCallback | None:
        action_callback = self.action_callbacks.get(action_id)
        if action_callback:
            return action_callback.callback
        return None

    def get_callback_callable(self, action_id: str) -> Callable:
        action_callback = self.action_callbacks.get(action_id)
        if action_callback:
            return action_callback.callback
        raise ValueError(f'No callback found for action_id: {action_id}')

    def add_callback(self, action_id: str, callback: Callable):
        self.action_callbacks[action_id] = ActionCallback(
            action_id=action_id, callback=callback
        )

    def create_callback(self, function: Callable) -> str:
        action_id = str(uuid.uuid4())
        self.register(action_id, function)
        return action_id

    def delete_callback(self, action_id: str) -> None:
        del self.action_callbacks[action_id]

    # def save(self) -> list[dict]:
    #     callbacks = []
    #     for action_id, action_callback in self.action_callbacks.items():
    #         callbacks.append({'action_id': action_id, **action_callback.model_dump()})
    #     return callbacks
