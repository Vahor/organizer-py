from state import State, add_log, config

from rich.console import Console, ConsoleOptions, RenderResult
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text
from rich.logging import RichHandler
from time import sleep
from io import StringIO
import logging


log_buffer = StringIO()
console = Console(file=log_buffer, width=100)

handler = RichHandler(console=console, rich_tracebacks=True)
logging.basicConfig(level=logging.DEBUG, format="%(message)s", handlers=[handler])
log = logging.getLogger(__name__)


def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=2),
        Layout(name="logs", ratio=1),
    )
    return layout


class Header:
    """Display header with clock."""

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]Organizer[/b]",
        )
        return Panel(grid, style="white")


class HelpBar:
    """Display help bar at the bottom of logs panel."""

    def __rich__(self) -> str:
        help_text = f"[b]{config.shortcut.quit}[/b]: quit • [b]{config.shortcut.next}[/b]: next • [b]{config.shortcut.prev}[/b]: previous • by [b]github.com/vahor[/b]"
        return help_text


class Logs:
    """Display scrollable logs."""

    state: State

    def __init__(self, state: State):
        self.state = state

    def __rich_console__(self, _: Console, options: ConsoleOptions) -> RenderResult:
        logs = self.state.get("logs", [])
        max_visible = (options.height or 4) - 4
        display_logs = logs[-max_visible:]

        if not display_logs:
            content = Text("No logs yet...", style="dim")
        else:
            content = Text(end="")
            for log in display_logs:
                timestamp = log.get("timestamp", "")
                message = log.get("message", "")
                level = log.get("level", "info")

                # Color based on level
                if level == "error":
                    line_color = "red"
                elif level == "success":
                    line_color = "green"
                else:
                    line_color = "white"

                content.append(f"[{timestamp}] ", style="dim")
                content.append(f"{message}\n", style=line_color)

        yield Panel(
            content,
            title="Logs",
            style="white",
            border_style="white",
            title_align="left",
            height=options.height,
        )


class Body:
    """Display body."""

    state: State

    def __init__(self, state: State):
        self.state = state

    def __rich__(self) -> Panel:
        table = Table(
            show_header=True, header_style="bold magenta", expand=True, box=None
        )
        table.add_column("Position", style="bold")
        table.add_column("Shortcut")
        table.add_column("Window", ratio=1)

        current_index = self.state["current_index"]
        for position, window in config.organizer.windows.items():
            if not window:
                continue

            is_active = position == current_index
            pos_col = f"[green]{position}[/green]" if is_active else f"{position}"
            table.add_row(pos_col, config.shortcut[f"_{position}"], window.name())

        return Panel(table, style="white", border_style="none", padding=(0, 0))


def start_ui(state: State):
    layout = make_layout()
    layout["header"].update(Header())
    layout["main"].update(Body(state))

    # Create a layout for logs section with help bar at bottom
    logs_layout = Layout(name="logs")
    logs_layout.split(
        Layout(name="logs_content", ratio=1),
        Layout(name="help", size=1),
    )
    logs_layout["logs_content"].update(Logs(state))  # type: ignore
    logs_layout["help"].update(HelpBar())
    layout["logs"].update(logs_layout)

    with Live(layout, refresh_per_second=10, screen=True):
        while not state["quitting"]:
            sleep(0.2)
            for line in log_buffer.getvalue().split("\n"):
                if line:
                    add_log(state, line, "info")
