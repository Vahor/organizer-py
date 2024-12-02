import subprocess
import json
from config import Window
from threading import Thread, Lock

mutex = Lock()

def get_window_by_name(query: Window):
    print(f"Searching for window: {query}")
    try:
        # Search for the window by name
        app_name = (query.app_name or '').lower()
        title = (query.title or '').lower()

        if len(app_name) == 0 and len(title) == 0:
            return None

        # Run the Yabai query to get all windows in JSON format
        result = subprocess.run(
            ['yabai', '-m', 'query', '--windows'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Check if the query ran successfully
        if result.returncode != 0:
            print(f"Error running Yabai: {result.stderr}")
            return None

        # Parse the JSON result
        windows = json.loads(result.stdout)

        for window in windows:
            window_app_name = window.get('app', '').lower()
            window_title = window.get('title', '').lower()

            app_name_match = len(app_name) == 0 or app_name in window_app_name
            title_match = len(title) == 0 or title in window_title
            if app_name_match and title_match:
                return window

        return None  # If no window is found with the given name
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def focus_window_by_name(query: Window):
    with mutex:
        if not query:
            return False
        window = get_window_by_name(query)
        if window:
            subprocess.run(['yabai', '-m', 'window', '--focus', str(window['id'])])
            return True

        print(f"Window not found: {query}")
