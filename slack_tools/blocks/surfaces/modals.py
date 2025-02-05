from dataclasses import dataclass, field
from typing import Any, Final, Literal, Self

from slack_tools.blocks.schemas.base import BaseLayout, BaseSurface
from slack_tools.blocks.schemas.objects import PlainTextSchema


@dataclass
class ModalSurface(BaseSurface, block_type='modal'):
    """Modal Surface.

    References:
        - [🔗 Modal](https://api.slack.com/surfaces/modals)
    """

    type: Final[Literal['modal']] = 'modal'

    title: PlainTextSchema = field(
        metadata={
            'title': 'title',
            'description': """
                The title that appears in the top-left of the modal.

            Validation:
                - Must be a plain_text text element with a max length of 24 characters.
            """,
            'max_length': 24,
        },
    )

    blocks: list[BaseLayout] = field(default_factory=list)

    close: PlainTextSchema | None = field(
        default=None,
        metadata={
            'title': 'close',
            'description': """
                An optional plain_text element that defines the text displayed in the
                close button at the bottom-right of the view.

            Validation:
                - Max length of 24 characters.
            """,
            'max_length': 24,
        },
    )

    submit: PlainTextSchema | None = field(
        default=None,
        metadata={
            'title': 'submit',
            'description': """
                An optional plain_text element that defines the text displayed
                in the submit button at the bottom-right of the view. submit is required
                when an input block is within the blocks array.

        Validation:
                - Max length of 24 characters.
            """,
            'max_length': 24,
        },
    )
    private_metadata: str | None = field(
        default=None,
        metadata={
            'title': 'private_metadata',
            'description': """
                An optional string that will be sent to your app in view_submission and
                block_actions events.

            Validation:
                - Max length of 3000 characters.
            """,
            'max_length': 3000,
        },
    )

    clear_on_close: bool = field(
        default=False,
        metadata={
            'title': 'clear_on_close',
            'description': """
                When set to true, clicking on the close button will clear all views in a
                modal and close it. Defaults to false.
            """,
        },
    )

    notify_on_close: bool = field(
        default=False,
        metadata={
            'title': 'notify_on_close',
            'description': """
                When set to true, Slack will send your request URL a view_closed event
                when a user clicks the close button. Defaults to false.
            """,
        },
    )

    external_id: str | None = field(
        default=None,
        metadata={
            'title': 'external_id',
            'description': """
                A custom identifier that must be unique for all views on a per-team basis.

                Validation:
                    - Max length of 255 characters.
            """,
            'max_length': 255,
        },
    )

    submit_disabled: bool = field(
        default=False,
        metadata={
            'title': 'submit_disabled',
            'description': """
                When set to true, disables the submit button until the user has completed
                one or more inputs. This property is for configuration modals. Defaults to
                false.
            """,
        },
    )

    def __getitem__(self, blocks: Any | tuple[Any, ...]) -> Self:
        """Add blocks to the Modal."""
        if not isinstance(blocks, tuple):
            blocks = (blocks,)

        for block in blocks:
            if hasattr(block, 'get_action') and callable(getattr(block, 'get_action')):
                callback = block.get_action()
                if callback:
                    self.action_handler.add_callback(
                        callback.action_id,
                        callback.callback,
                    )

        self.blocks.extend(blocks)
        return self
