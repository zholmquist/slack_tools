import json
import re
from dataclasses import asdict
from urllib.parse import quote

from slack_tools.blocks.mixins.copyable import CopyableStrMixin
from slack_tools.utils.dataclass_utils import remove_none


class SlackBlockKitPreviewURL(CopyableStrMixin):
    """Slack BlockKit Preview URL."""

    def __str__(self) -> str:
        return self

    def __repr__(self) -> str:
        return self


class BlockKitPreviewMixin:
    """Mixin to allow previewing blocks.

    # TODO: Add team_id to the URL /#{team_id}
    """

    _base_url = 'https://app.slack.com/block-kit-builder/#'

    def as_builder_url(self, team_id: str | None = None) -> SlackBlockKitPreviewURL:
        """Generates a URL to preview the block in Slack's Block Kit Builder."""
        block_dict = asdict(self)
        block_dict = remove_none(block_dict)

        # Wrap blocks in the expected format if not already wrapped
        if 'blocks' not in block_dict:
            block_dict = {
                'blocks': block_dict['blocks']
                if 'blocks' in block_dict
                else [block_dict]
            }

        block_json = json.dumps(
            block_dict, separators=(',', ':')
        )  # Remove spaces from JSON
        encoded_blocks = self._url_encode_blocks(block_json)

        # Return a class?
        return SlackBlockKitPreviewURL(f'{self._base_url}{encoded_blocks}')

    def _url_encode_blocks(self, json_blocks: str) -> str:
        """Encode the blocks for the builder URL."""
        # First do standard URL encoding
        encoded_blocks = quote(json_blocks, safe=':')  # Keep colons unencoded

        # Then handle special characters that need custom encoding
        special_chars_pattern = r'[!\'()*]'
        encoded_blocks = re.sub(
            special_chars_pattern,
            lambda m: '%' + hex(ord(m.group(0)))[2:].upper(),
            encoded_blocks,
        )

        return encoded_blocks
