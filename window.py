import subprocess
import json
from config import Window

def get_window_by_name(query: Window):
    try:
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

        # Search for the window by name
        app_name = (query.app_name or '').lower()
        title = (query.title or '').lower()
        for window in windows:
            if app_name and app_name in window.get('app', '').lower():
                return window
            if title and title in window.get('title', '').lower():
                return window

        return None  # If no window is found with the given name
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def focus_window_by_name(query: Window):
    window = get_window_by_name(query)
    if window:
        subprocess.run(['yabai', '-m', 'window', '--focus', str(window['id'])])

