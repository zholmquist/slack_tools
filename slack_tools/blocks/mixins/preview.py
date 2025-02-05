import json
import re
from dataclasses import asdict
from urllib.parse import quote


class BlockKitPreviewMixin:
    """Mixin to allow previewing blocks.

    # TODO: Add team_id to the URL /#{team_id}
    """

    _base_url = 'https://app.slack.com/block-kit-builder/#'

    def as_builder_url(self, team_id: str | None = None) -> str:
        """Generates a URL to preview the block in Slack's Block Kit Builder."""
        preview_data = json.dumps(asdict(self))
        encoded_blocks = self._url_encode_blocks(preview_data)
        return f'{self._base_url}{encoded_blocks}'

    def _url_encode_blocks(self, json_blocks: str) -> str:
        """Encode the blocks for the builder URL."""
        encoded_blocks = quote(json_blocks)
        special_chars_pattern = r'[!\'()*]'
        encoded_blocks = re.sub(
            special_chars_pattern,
            lambda m: '%' + hex(ord(m.group(0)))[2:].upper(),
            encoded_blocks,
        )
        return encoded_blocks
