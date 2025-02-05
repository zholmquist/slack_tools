import json
from dataclasses import asdict, is_dataclass

from slack_tools.utils.dataclass_utils import remove_none


class SerializableMixin:
    """Mixin for serializing dataclasses."""

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
        dict_repr = remove_none(self.to_dict())
        return json.dumps(dict_repr)
