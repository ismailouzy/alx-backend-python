#!/usr/bin/env python3
"""Unit tests for utils module."""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from typing import Any, Dict, Tuple, Union
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
            self, nested_map: Dict,
            path: Tuple[str, ...], expected: Union[Dict, int]) -> None:
        """Test access_nested_map returns correct output."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "KeyError: 'a'"),
        ({"a": 1}, ("a", "b"), "KeyError: 'b'"),
    ])
    def test_access_nested_map_exception(
            self, nested_map: Dict,
            path: Tuple[str, ...], exception_message: str) -> None:
        """Test access_nested_map raises correct exception."""
        with self.assertRaisesRegex(KeyError, exception_message):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests for get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(
            self, test_url: str, test_payload: Dict[str, bool]) -> None:
        """Test get_json returns correct output."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        with patch('requests.get', return_value=mock_response) as mock_get:
            self.assertEqual(get_json(test_url), test_payload)
            mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Tests for memoize decorator."""

    def test_memoize(self) -> None:
        """Test memoize decorator."""
        class TestClass:
            def a_method(self) -> int:
                return 42

            @memoize
            def a_property(self) -> int:
                return self.a_method()

        test_obj = TestClass()
        with patch.object(TestClass, 'a_method', return_value=42,
                          ) as mocked_method:
            result1 = test_obj.a_property
            result2 = test_obj.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mocked_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
