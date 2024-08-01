#!/usr/bin/env python3
"""
type-annotated function element_length
"""
from typing import Iterable, List, Tuple, Sequence


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    return a list of tuples
    """
    return [(i, len(i)) for i in lst]
