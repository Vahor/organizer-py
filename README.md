# Organizer

Organizer is a Python tool to focus your windows with keyboard shortcuts.

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
title = "chatgpt"

[organizer.2]
app_name = "discord"

[organizer.3]
title = "spotify"
```

Here's a description of the configuration options:

| Block                | Field     | Description                                             |
| ---                  | ---       | ---                                                     |
| `shortcut`           | next      | The keyboard shortcut to switch to the next window.     |
| `shortcut`           | prev      | The keyboard shortcut to switch to the previous window. |
| `organizer.[number]` | app_name? | The name of the application.                            |
| `organizer.[number]` | title?    | The title of the window.                                |

The tool will search open windows for the specified application and title, and switch to the first one it finds.
`app_name` and `title` are optional, and can be used to narrow down the search.
`number` is the order in which the windows will be switched, should be unique.


