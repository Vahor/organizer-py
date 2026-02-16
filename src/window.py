import subprocess
import json
from config import Window
from state import add_log


def get_window_by_name(query: Window, state):
    try:
        # Search for the window by name
        app_name = (query.app_name or "").lower()
        title = (query.title or "").lower()

        if len(app_name) == 0 and len(title) == 0:
            return None

        # Run the Yabai query to get all windows in JSON format
        result = subprocess.run(
            ["yabai", "-m", "query", "--windows"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Check if the query ran successfully
        if result.returncode != 0:
            add_log(state, f"Yabai error: {result.stderr}", "error")
            return None

        # Log any stderr output from yabai (warnings, info, etc.)
        if result.stderr:
            add_log(state, f"Yabai: {result.stderr.strip()}", "info")

        # Parse the JSON result
        windows = json.loads(result.stdout)

        for window in windows:
            window_app_name = window.get("app", "").lower()
            window_title = window.get("title", "").lower()

            app_name_match = len(app_name) == 0 or app_name in window_app_name
            title_match = len(title) == 0 or title in window_title
            if app_name_match and title_match:
                return window

        add_log(state, f"Window not found: {query}", "info")
        return None  # If no window is found with the given name
    except Exception as e:
        add_log(state, f"Error getting window: {e}", "error")
        return None


def focus_window_by_name(query: Window, state):
    if not query:
        add_log(state, "No window query provided", "error")
        return False
    window = get_window_by_name(query, state)
    if window:
        result = subprocess.run(
            ["yabai", "-m", "window", "--focus", str(window["id"])],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Log any stderr output from yabai
        if result.stderr:
            add_log(state, f"Yabai: {result.stderr.strip()}", "info")

        if result.returncode != 0:
            add_log(state, f"Failed to focus window: {result.stderr}", "error")
            return False

        return True
    else:
        add_log(state, f"Window not found: {query}", "error")
        return False
