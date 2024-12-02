from config import load_config
from window import focus_window_by_name
from pynput import keyboard

current_index = 1

def next_index():
    global current_index
    current_index = (current_index + 1) % len(config.organizer.windows)
    if current_index == 0:
        current_index = len(config.organizer.windows)
    return current_index

def prev_index():
    global current_index
    current_index = (current_index - 1) % len(config.organizer.windows)
    if current_index == 0:
        current_index = len(config.organizer.windows)
    return current_index

if __name__ == "__main__":
    config = load_config()

    # TODO: nice print with config and help
    # for window in config.organizer.windows.values():
    #     found = get_window_by_name(window)
    #     print(window, found.get('title') if found else 'not found')

    hotkeys = {
        "q": lambda: print("todo"),
        # TODO: don't know why but doing this in a loop doesn't work
        config.shortcut._1: lambda: focus_window_by_name(config.organizer.windows[1]),
        config.shortcut._2: lambda: focus_window_by_name(config.organizer.windows[2]),
        config.shortcut._3: lambda: focus_window_by_name(config.organizer.windows[3]),
        config.shortcut._4: lambda: focus_window_by_name(config.organizer.windows[4]),
        config.shortcut._5: lambda: focus_window_by_name(config.organizer.windows[5]),
        config.shortcut._6: lambda: focus_window_by_name(config.organizer.windows[6]),
        config.shortcut._7: lambda: focus_window_by_name(config.organizer.windows[7]),
        config.shortcut._8: lambda: focus_window_by_name(config.organizer.windows[8]),
        config.shortcut._9: lambda: focus_window_by_name(config.organizer.windows[9]),
        config.shortcut.next: lambda: focus_window_by_name(config.organizer.windows[next_index()]),
        config.shortcut.prev: lambda: focus_window_by_name(config.organizer.windows[prev_index()]),
    }

    with keyboard.GlobalHotKeys(hotkeys) as h:
        h.join()
