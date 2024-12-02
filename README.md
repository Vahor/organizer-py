# Organizer

Organizer is a Python tool to focus your windows with keyboard shortcuts.\

**Example:** Open Firefox by pressing `ctrl+1`, discord by pressing `ctrl+2`, etc, and go back to the previous window by pressing `page_down`.

![Preview](https://github.com/user-attachments/assets/5cab85de-d330-4a16-a393-d29ddf6316a3)

## Requirements

- Python 3.10+
- Yabai: https://github.com/koekeishiya/yabai
- Poetry: https://python-poetry.org/docs/ _(optional, you can use `pip` instead and install the dependencies manually)_
- Poe: https://github.com/nathan-ho/poe _(optional, you can run the `script` directly)_

## How to use

1. Clone the repository
2. Install the dependencies: `poetry install` or `pip install pynput toml rich`
3. Run the script: `poetry run python src/app.py` or `poe run`

## Configuration

Edit the `config.toml` file to configure the shortcuts.

```toml title="config.toml"
[shortcut]
next = "<shift>+1"
prev = "<shift>+2"
1    = "<ctrl>+1"
2    = "<ctrl>+2"
3    = "<ctrl>+3"
4    = "<ctrl>+4"
5    = "<ctrl>+5"
6    = "<ctrl>+6"
7    = "<ctrl>+7"
8    = "<ctrl>+8"
9    = "<ctrl>+9"

[organizer.1]
app_name = "firefox"
title = "vahor"

[organizer.2]
app_name = "discord"

[organizer.3]
title = "spotify"
```

Here's a description of the configuration options:

| Block                | Field      | Description                                              |
| ---                  | ---        | ---                                                      |
| `shortcut`           | next       | The keyboard shortcut to switch to the next window.      |
| `shortcut`           | prev       | The keyboard shortcut to switch to the previous window.  |
| `shortcut`           | `[number]` | The keyboard shortcut to switch to the specified window. |
| `organizer.[number]` | app_name?  | The name of the application.                             |
| `organizer.[number]` | title?     | The title of the window.                                 |

The tool will search open windows for the specified application and title, and switch to the first one it finds.\
`app_name` and `title` are optional, and can be used to narrow down the search.\
`number` is the order in which the windows will be switched, should be unique.

You can find a full list of keyboard shortcuts [here](https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key).


