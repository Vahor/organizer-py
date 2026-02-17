from multiprocessing import Queue
import signal
import sys

from state import State, config, add_log
from time import sleep

from pynput import keyboard


def _next_index(state: State):
    idx = state["current_index"]
    while True:
        idx = (idx + 1) % len(config.organizer.windows)
        if idx == 0:
            idx = len(config.organizer.windows)
        if config.organizer.windows.get(idx):
            break

    state["current_index"] = idx
    return idx


def _prev_index(state: State):
    idx = state["current_index"]
    while True:
        idx = (idx - 1) % len(config.organizer.windows)
        if idx == 0:
            idx = len(config.organizer.windows)
        if config.organizer.windows.get(idx):
            break

    state["current_index"] = idx
    return idx


def setup_hotkeys(state: State, window_queue: Queue):

    def quit_app():
        add_log(state, "Goodbye!", "success")
        state["quitting"] = True
        sys.exit(0)

    def signal_handler(signum, frame):
        quit_app()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    def focus_window_by_name_wrapper(query):
        add_log(state, f"Focusing {query.name()}...", "info")
        window_queue.put((query.app_name, query.title))

    hotkeys = {
        config.shortcut.quit: lambda: quit_app(),
        # TODO: don't know why but doing this in a loop doesn't work
        config.shortcut._1: lambda: focus_window_by_name_wrapper(
            config.organizer.windows[1]
        ),
        config.shortcut._2: lambda: focus_window_by_name_wrapper(
            config.organizer.windows[2]
        ),
        config.shortcut._3: lambda: focus_window_by_name_wrapper(
            config.organizer.windows[3]
        ),
        config.shortcut._4: lambda: focus_window_by_name_wrapper(
            config.organizer.windows[4]
        ),
        config.shortcut._5: lambda: focus_window_by_name_wrapper(
            config.organizer.windows[5]
        ),
        config.shortcut._6: lambda: focus_window_by_name_wrapper(
            config.organizer.windows[6]
        ),
        config.shortcut._7: lambda: focus_window_by_name_wrapper(
            config.organizer.windows[7]
        ),
        config.shortcut._8: lambda: focus_window_by_name_wrapper(
            config.organizer.windows[8]
        ),
        config.shortcut._9: lambda: focus_window_by_name_wrapper(
            config.organizer.windows[9]
        ),
        config.shortcut.next: lambda: focus_window_by_name_wrapper(
            config.organizer.windows[_next_index(state)]
        ),
        config.shortcut.prev: lambda: focus_window_by_name_wrapper(
            config.organizer.windows[_prev_index(state)]
        ),
    }

    try:
        with keyboard.GlobalHotKeys(hotkeys) as h:
            h.join()
    except KeyboardInterrupt:
        quit_app()
    except Exception as e:
        add_log(state, f"Caught exception: {e}", "error")
        add_log(state, "Exiting in 5 seconds...", "error")
        sleep(5)
        quit_app()
