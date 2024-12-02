from config import load_config
from window import focus_window_by_name


if __name__ == "__main__":
    config = load_config()
    focus_window_by_name(config.organizer.windows[3])
