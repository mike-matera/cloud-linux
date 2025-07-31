"""
Random processes.
"""

import datetime
from typing import Any, Callable

import psutil

from kroz.random import choice


def random_process(
    filter: Callable[[dict[str, Any]], bool],
) -> dict[str, Any]:
    """
    Return a random process running on the system. In order to make it more
    likely that the process will still be running when a student answers a
    question the process will be more than five minutes old.
    """
    min_age = datetime.timedelta(minutes=5)
    fields = [
        "pid",
        "ppid",
        "name",
        "terminal",
        "memory_percent",
        "nice",
        "status",
        "username",
        "cmdline",
        "create_time",
        "cwd",
        "exe",
    ]

    candidates = {
        process.pid: process.info
        for process in psutil.process_iter(fields)
        if datetime.datetime.now()
        - datetime.datetime.fromtimestamp(process.info["create_time"])
        > min_age
        and filter(process.info)
    }
    return choice(candidates)
