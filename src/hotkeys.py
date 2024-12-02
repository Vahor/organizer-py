from state import State, config

from window import focus_window_by_name
from pynput import keyboard

def _next_index(state: State):
    idx = state["current_index"]
    idx = (idx + 1) % len(config.organizer.windows)
    if idx == 0:
        idx = len(config.organizer.windows)

    state["current_index"] = idx
    return idx

def _prev_index(state: State):
    idx = state["current_index"]
    idx = (idx - 1) % len(config.organizer.windows)
    if idx == 0:
        idx = len(config.organizer.windows)

    state["current_index"] = idx
    return idx

def setup_hotkeys(state: State):

    def quit_app():
        state["status_message"] = "Quitting..."
        state["quitting"] = True
        exit(0)

    def focus_window_by_name_wrapper(query):
        state["status_message"] = f"Focusing {query.name()}..."
        if not focus_window_by_name(query):
            state["status_message"] = f"[red]Error: Could not find window with name [b]{query.name()}[/b][/red]"


    hotkeys = {
        "q": lambda: quit_app(),
        # TODO: don't know why but doing this in a loop doesn't work
        config.shortcut._1: lambda: focus_window_by_name_wrapper(config.organizer.windows[1]),
        config.shortcut._2: lambda: focus_window_by_name_wrapper(config.organizer.windows[2]),
        config.shortcut._3: lambda: focus_window_by_name_wrapper(config.organizer.windows[3]),
        config.shortcut._4: lambda: focus_window_by_name_wrapper(config.organizer.windows[4]),
        config.shortcut._5: lambda: focus_window_by_name_wrapper(config.organizer.windows[5]),
        config.shortcut._6: lambda: focus_window_by_name_wrapper(config.organizer.windows[6]),
        config.shortcut._7: lambda: focus_window_by_name_wrapper(config.organizer.windows[7]),
        config.shortcut._8: lambda: focus_window_by_name_wrapper(config.organizer.windows[8]),
        config.shortcut._9: lambda: focus_window_by_name_wrapper(config.organizer.windows[9]),
        config.shortcut.next: lambda: focus_window_by_name_wrapper(config.organizer.windows[_next_index(state)]),
        config.shortcut.prev: lambda: focus_window_by_name_wrapper(config.organizer.windows[_prev_index(state)]),
    }

    with keyboard.GlobalHotKeys(hotkeys) as h:
        h.join()

