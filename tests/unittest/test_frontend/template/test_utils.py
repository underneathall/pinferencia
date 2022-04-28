from unittest.mock import MagicMock

import pytest

from pinferencia.frontend.templates.utils import display_text_prediction


@pytest.mark.parametrize(
    "data_and_display_type",
    [
        ([{"a": 1, "b": 2}, {"a": 3, "b": 4}], "table"),
        ([{"a": 1, "b": 2}, {"c": 3, "d": 4, "e": 5}], "table"),
        ([{"a": 1, "b": 2}, 1, 2], "json"),
        ([1, 2, 3], "json"),
        ({"a": 1}, "json"),
        (1, "json"),
        ("abcd", "info"),
    ],
)
def test_display_text_prediction(data_and_display_type):
    data, display_type = data_and_display_type
    component = MagicMock()
    display_text_prediction(data, component)
    assert getattr(component, display_type).called
