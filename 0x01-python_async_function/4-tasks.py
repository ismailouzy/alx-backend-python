#!/usr/bin/env python3
"""
task2
"""
import asyncio
from typing import List
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    The function returns a list of floats.
    Each float in the list represents the amount of time (s)
    The list is automatically sorted in ascending order
    due to the use of asyncio.as_completed().
"""
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    delays = []
    for future in asyncio.as_completed(tasks):
        delay = await future
        delays.append(delay)
    return delays
