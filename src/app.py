import state

from hotkeys import setup_hotkeys
from window import window_worker
from ui import start_ui
from multiprocessing import Process, Manager, Queue
from datetime import datetime
from rich.console import Console

console = Console()


if __name__ == "__main__":
    with Manager() as manager:
        state = manager.dict()
        state["current_index"] = 1
        state["quitting"] = False
        state["logs"] = manager.list(
            [
                {
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "message": "Application started",
                    "level": "success",
                }
            ]
        )

        window_queue = Queue()

        p_hotkeys = Process(target=setup_hotkeys, args=(state,window_queue))
        p_ui = Process(target=start_ui, args=(state,))
        p_window = Process(target=window_worker, args=(window_queue, state))

        p_hotkeys.start()
        p_ui.start()
        p_window.start()

        try:
            p_hotkeys.join()
            p_ui.join()
        except KeyboardInterrupt:
            pass
        finally:
            window_queue.put(None)
            p_window.terminate()
            p_hotkeys.terminate()
            p_ui.terminate()
            p_window.join()
            p_hotkeys.join()
            p_ui.join()

        console.show_cursor(True)
        console.clear()
