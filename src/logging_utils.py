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
        for line in result.stdout.strip().split("\n"):
            if line.strip():
                add_log(state, line.strip(), log_level)

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            if line.strip():
                add_log(state, line.strip(), error_level)

    return result


