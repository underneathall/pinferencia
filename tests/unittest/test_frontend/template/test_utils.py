from unittest.mock import MagicMock

import pytest

from pinferencia.frontend.templates.utils import (
    display_text_prediction,
    format_data_with_type_hint_str,
    is_list_type,
)


@pytest.mark.parametrize(
    "data_and_display_type",
    [
        ([{"a": 1, "b": 2}, {"a": 3, "b": 4}], "table"),
        ([{"a": 1, "b": 2}, {"c": 3, "d": 4, "e": 5}], "table"),
        ([{"a": 1, "b": 2}, 1, 2], "json"),
        ([1, 2, 3], "json"),
        ({"a": 1}, "json"),
        (1, "info"),
        ("abcd", "info"),
    ],
)
def test_display_text_prediction(data_and_display_type):
    data, display_type = data_and_display_type
    component = MagicMock()
    display_text_prediction(data, component)
    assert getattr(component, display_type).called


@pytest.mark.parametrize(
    "type_and_result",
    [
        ("str", False),
        ("int", False),
        ("float", False),
        ("bool", False),
        ("list", True),
        ("list[str]", True),
        ("list[int]", True),
        ("list[float]", True),
        ("list[bool]", True),
        ("typing.List", True),
        ("typing.List[str]", True),
        ("typing.List[int]", True),
        ("typing.List[float]", True),
        ("typing.List[bool]", True),
    ],
)
def test_is_list_type(type_and_result):
    type_str, result = type_and_result
    assert is_list_type(type_str) == result


@pytest.mark.parametrize(
    "args_and_result",
    [
        ((1, "str"), "1"),
        ((1, "int"), 1),
        ((1, "bool"), True),
        (([1], "list"), [1]),
        (([1], "typing.List"), [1]),
        (([1], "typing.List[str]"), ["1"]),
        (([1], "typing.List[float]"), [1.0]),
    ],
)
def test_format_data_with_type_hint_str(args_and_result):
    input_args, result = args_and_result
    assert format_data_with_type_hint_str(*input_args) == result
