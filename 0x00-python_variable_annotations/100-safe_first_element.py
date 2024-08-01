#!/usr/bin/env python3
"""
duck-typed annotations
"""
from typing import Sequence, Any, Union, Optional


def safe_first_element(lst: Sequence[Any]) -> Optional[Any]:
    """
    This function takes a sequence and returns its first element if the sequence
    is not empty. If the sequence is empty, it returns None.
    """
    if lst:
        return lst[0]
    else:
        return None
