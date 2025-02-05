from rich.console import Console

from slack_tools.block_kit import BlockKit

console = Console()

bk = BlockKit()


layout = bk[
    bk.header('Hello'),
    bk.section(
        'Hello',
        accessory=bk.button('Click me', action_id='click_me'),
    ),
    bk.divider(),
    bk.section('Hello'),
]

# As JSON
console.print_json(layout.to_json())

# As Python Objects
console.print(layout.to_dict())

# As Builder URL
console.print(layout.as_builder_url())
