from slack_tools.block_kit import BlockKit
from slack_tools.mrkdwn_kit import Markdown


def greet_one():
    """Callback for a button passed directly to a Button."""
    print('Hi! I was passed directly.', end='\n\n')


def greet_two():
    """Callback for a button passed with .action()."""
    print('Hello! I was passed with .action()', end='\n\n')


# Initialize BlockKit
bk = BlockKit()

# Initialize Markdown
md = Markdown()

# Passing a callback directly to a Button
button_with_callback = bk.button('🟠 Click me', callback=greet_one)
callback_action_id = button_with_callback.action_id

# Passing a callback with .action()
button_with_action = bk.button('🔵 Click me')
button_with_action.action(greet_two)
action_id = button_with_action.action_id

# Layout
layout = bk[
    bk.header('Hello'),
    bk.section(
        'Hello',
        accessory=button_with_callback,
    ),
    bk.divider(),
    bk.section(
        md.strikethrough('Hello'),
        accessory=button_with_action,
    ),
    bk.divider(),
    bk.section(
        md.bold('Hello'),
        accessory=bk.button('🟣 Click me', action_id='action-id', callback=greet_one),
    ),
    bk.divider(),
]


if __name__ == '__main__':
    # Callback Demo
    from rich import print

    print('\nCallback Demo...', end='\n\n')
    if callback_action_id:
        callback_one = bk.get_callback_fn(callback_action_id)
        callback_one()

    if action_id:
        callback_two = bk.get_callback_fn(action_id)
        callback_two()

    # Layout Demo
    callback_three = bk.get_callback_fn('action-id')
    callback_three()

    # Print markdown text directly
    print(layout.to_json())
