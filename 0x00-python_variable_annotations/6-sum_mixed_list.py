#!/usr/bin/env python3
"""
type-annotated function sum_mixed_list
"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[float, int]]) -> float:
    """
    return the sum of a list
    """
    return sum(mxd_lst)
