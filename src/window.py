from state import add_log
from multiprocessing import Queue

import AppKit
import ApplicationServices

_cache: dict = {}


def get_window_for_app(ax_app, title):
    err, windows = ApplicationServices.AXUIElementCopyAttributeValue(
        ax_app, "AXWindows", None
    )

    if err or not windows:
        return None

    for window in windows:
        err, window_title = ApplicationServices.AXUIElementCopyAttributeValue(
            window, "AXTitle", None
        )
        if (
            not err
            and window_title
            and title.lower() in window_title.lower()
        ):
            return window

    return None


def get_app(app_name, title):
    cache_key = f"{app_name}:{title}"

    # Try cached app/AX application first
    cached = _cache.get(cache_key)
    if cached:
        app = cached["app"]
        ax_app = cached["ax_app"]

        window = get_window_for_app(ax_app, title)
        if window:
            return app, ax_app, window

        # Fall through to a full search if cache is stale

    # No valid cache entry or cache was stale: search all matching apps,
    # and only cache the specific app whose window title matches.
    workspace = AppKit.NSWorkspace.sharedWorkspace()
    for app in workspace.runningApplications():
        if app.localizedName().lower() != app_name.lower():
            continue

        pid = app.processIdentifier()
        ax_app = ApplicationServices.AXUIElementCreateApplication(pid)

        window = get_window_for_app(
            ax_app,
            title,
        )
        if window:
            _cache[cache_key] = {"app": app, "ax_app": ax_app}
            return app, ax_app, window

    return None, None, None


def focus_app(app_name, title):
    app, ax_app, window = get_app(app_name, title)
    if not app or not window:
        return False

    app.activateWithOptions_(AppKit.NSApplicationActivateIgnoringOtherApps)
    ApplicationServices.AXUIElementPerformAction(window, "AXRaise")
    return True


def window_worker(queue: Queue, state):
    while True:
        try:
            item = queue.get()
            if item is None:  # shutdown signal
                break
            app_name, title = item
            if not focus_app(app_name, title):
                add_log(
                    state,
                    f"Could not focus app: {app_name} with title: {title}",
                    "error",
                )

        except Exception as e:
            add_log(state, f"Caught exception: {e}", "error")
