from config import load_config
from typing import TypedDict
from datetime import datetime

config = load_config()


class State(TypedDict):
    current_index: int
    quitting: bool
    logs: list


def add_log(state: State, message: str, level: str = "info") -> None:
    """Add a log entry to the state."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    state["logs"].append({"timestamp": timestamp, "message": message, "level": level})
