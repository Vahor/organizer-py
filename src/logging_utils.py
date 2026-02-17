"""Logging utilities to capture print and subprocess output."""

import subprocess
from state import State, add_log


def run_subprocess_with_logging(
    state: State,
    command: list[str],
    log_level: str = "info",
    error_level: str = "error",
    **kwargs,
) -> subprocess.CompletedProcess:
    result = subprocess.run(command, capture_output=True, text=True, **kwargs)

    # TODO: live logs
    if result.stdout:
        add_log(state, result.stdout.strip(), log_level)

    if result.stderr:
        add_log(state, result.stderr.strip(), error_level)

    return result
