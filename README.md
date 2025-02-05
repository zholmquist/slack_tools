# Slack Tools

A concise, and opinionated, syntax for building Slack Block Kit UIs.

> [!CAUTION]
> This project is not fully complete, and implementation details are unstable.

## Usage

```python
from slack_tools import BlockKit

# Button Action Callback
def greet():
    print('Hello!')

# Initialize BlockKit
bk = BlockKit()

# Construct Layout
layout = bk[
    bk.header('Hello'),
    bk.divider(),
    bk.section(
        'Hello',
        accessory=bk.button('🟣 Click me', action_id='action-id', callback=greet),
    ),
    bk.divider(),
]

# Print Layout as JSON with `{"blocks": ...}`
print(layout.to_json())

# For API Consumption
print(layout.to_api())
```
> [!NOTE]
> If running directly from terminal, you will need to run `uv sync` or `uv run <file_name>.py` to install the dependencies.


## Examples

See [examples](examples) for more.

# Supported Components
soon.
