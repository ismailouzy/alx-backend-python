#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map function."""

import unittest
from parameterized import parameterized
from typing import Dict, Union, Tuple
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Dict, path: Tuple[str], expected: Union[Dict, int]) -> None:
        """Test access_nested_map returns correct output."""
        self.assertEqual(access_nested_map(nested_map, path), expected)
