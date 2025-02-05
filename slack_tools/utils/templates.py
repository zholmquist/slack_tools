from pathlib import Path
from typing import Self

from jinja2 import Environment as JinjaEnvironment


class Template:
    _instance = None
    env = JinjaEnvironment()

    def __new__(cls, *args, **kwargs) -> Self:
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def render(self, template: str | Path, /, **kwargs):
        if isinstance(template, Path):  # TODO: Confirm `Path` loads file
            template = template.read_text()
        template_obj = self.env.from_string(template)
        return template_obj.render(**kwargs)
