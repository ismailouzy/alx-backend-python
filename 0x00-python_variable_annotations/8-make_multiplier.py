#!/usr/bin/env python3
"""
type-annotated function make_multiplier
"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    returns a function that multiplies a float
    """
    def multiplier_function(x: float) -> float:
        return x * multiplier
    return multiplier_function
