from dataclasses import dataclass
from typing import Callable


@dataclass
class CallbackFunction:
    name: str
    source: str


@dataclass
class ActionCallback:
    action_id: str
    callback: Callable
