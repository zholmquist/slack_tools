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

console.print(layout)
console.print_json(layout.to_json())
