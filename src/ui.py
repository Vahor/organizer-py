from state import State, config

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from time import sleep

console = Console()
console.clear()

def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3),
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

class Status:
    """Display status."""

    state: State
    def __init__(self, state: State):
        self.state = state

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right")

        help_text = f"[b]q[/b]: quit • [b]{config.shortcut.next}[/b]: next • [b]{config.shortcut.prev}[/b]: previous"
        grid.add_row(
            f"[b]Status:[/b] " + self.state["status_message"],
            f"{help_text} • by [b]github.com/vahor[/b]",
        )
        return Panel(grid, style="white")

class Body:
    """Display body."""

    state: State
    def __init__(self, state: State):
        self.state = state

    def __rich__(self) -> Panel:
        table = Table(show_header=True, header_style="bold magenta", expand=True, box=None)
        table.add_column("Position", style="bold")
        table.add_column("Shortcut")
        table.add_column("Window", ratio=1)

        current_index = self.state["current_index"]
        for position, window in config.organizer.windows.items():
            is_active = position == current_index
            pos_col = f"[green]{position}[/green]" if is_active else f"{position}"
            table.add_row(pos_col, config.shortcut[f'_{position}'], window.name())

        return Panel(table, style="white", border_style="none", padding=(0, 0))


def start_ui(state: State):
    layout = make_layout()
    layout["header"].update(Header())
    layout["main"].update(Body(state))
    layout["footer"].update(Status(state))

    timer = 0
    with Live(layout, refresh_per_second=1):
        while not state["quitting"]:
            if len(state["status_message"]) > 0:
                timer += 1
                if timer % 2 == 0:
                    state["status_message"] = "" 
                    timer = 0
            sleep(1)
    console.clear()

