import pytest

from slack_tools.blocks.schemas.blocks import ImageBlockSchema, SectionBlockSchema
from slack_tools.blocks.schemas.objects import PlainTextSchema


def test_section_block_type_validation():
    """Test that type validation works in section blocks."""
    # Test invalid type - should raise ValueError
    with pytest.raises(ValueError):
        SectionBlockSchema(
            text=PlainTextSchema(text='test'),
            accessory='not a valid type',  # This should fail validation
        )

    # Test valid types - should not raise any errors
    SectionBlockSchema(
        text=PlainTextSchema(text='test'),
        accessory=None,  # None is valid
    )

    SectionBlockSchema(
        text=PlainTextSchema(text='test'),
        accessory=ImageBlockSchema(  # ImageSchema is valid
            alt_text='test image', image_url='https://example.com/image.jpg'
        ),
    )
