import state

from hotkeys import setup_hotkeys
from ui import start_ui
from multiprocessing import Process, Manager
from datetime import datetime
from rich.console import Console

console = Console()


if __name__ == "__main__":
    with Manager() as manager:
        state = manager.dict()
        state["current_index"] = 1
        state["quitting"] = False
        state["logs"] = [
            {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "message": "Application started",
                "level": "success",
            }
        ]

        p_hotkeys = Process(target=setup_hotkeys, args=(state,))
        p_hotkeys.start()
        p_ui = Process(target=start_ui, args=(state,))
        p_ui.start()

        try:
            p_hotkeys.join()
            p_ui.join()
        except KeyboardInterrupt:
            pass
        finally:
            p_hotkeys.terminate()
            p_ui.terminate()
            p_hotkeys.join()
            p_ui.join()

        console.show_cursor(True)
        console.clear()
