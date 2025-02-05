from slack_tools.blocks.schemas.objects import OptionSchema
from slack_tools.blocks.text import PlainText


class Option(OptionSchema):
    @classmethod
    def create(
        cls,
        text: str,
        /,
        *,
        value: str,
        description: str | None = None,
        url: str | None = None,
    ):
        """Create an option block."""
        return cls(
            text=PlainText(text=text),
            value=value,
            description=PlainText(text=description) if description else None,
            url=url,
        )
