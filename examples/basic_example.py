from rich.console import Console
from rich.json import JSON

from slack_tools.block_kit import BlockKit
from slack_tools.mrkdwn_kit import MarkdownKit

console = Console()

bk = BlockKit()
md = MarkdownKit()

layout = bk[
    bk.header('Hello'),
    bk.section(
        md.bold('Hello'),
        accessory=bk.button('Click me', action_id='click_me_1'),
    ),
    bk.section(md.compose(md.bold('Hello'))),
    bk.divider(),
    bk.section('Hello'),
    bk.actions[
        bk.button('🦑 Click me', action_id='click_me_2', style='primary'),
        bk.button('Click me', action_id='click_me_3'),
    ],
    bk.rich_text[
        bk.rich_text_section[md.bold('hello'), md.strikethrough('hello'), md.bold('world')],
        bk.rich_text_list[
            bk.rich_section['hello'],
            bk.rich_section['world'],
        ].styles(ordered=True, indent=7),
    ],
]

# As JSON
console.print_json(layout.to_json())

# As Python Objects
console.print(JSON(layout.to_json()))

# As Builder URL
console.print(layout.as_builder_url())
