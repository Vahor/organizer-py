from config import load_config
from typing import TypedDict

config = load_config()

class State(TypedDict):
    current_index: int 
    quitting: bool 
    status_message: str
