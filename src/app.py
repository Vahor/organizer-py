import state

from hotkeys import setup_hotkeys
from ui import start_ui
from multiprocessing import Process, Manager
from config import Config, load_config


if __name__ == "__main__":
    with Manager() as manager:

        state = manager.dict()
        state["current_index"] = 1
        state["quitting"] = False
        state["status_message"] = "Starting..."


        p_hotkeys = Process(target=setup_hotkeys, args=(state,))
        p_hotkeys.start()
        p_ui = Process(target=start_ui, args=(state,))
        p_ui.start()

        p_hotkeys.join()
        p_ui.join()

        # TODO: nice print with config and help
        # for window in config.organizer.windows.values():
        #     found = get_window_by_name(window)
        #     print(window, found.get('title') if found else 'not found')


