from unittest.mock import MagicMock

import pytest

from pinferencia.frontend.templates.base import BaseTemplate, st


class TestTemplate(BaseTemplate):
    title = "My Test Template"


def test_render_header(monkeypatch):
    markdown_mock = MagicMock()
    monkeypatch.setattr(st, "markdown", markdown_mock)

    # initialize the template and render the header
    tmpl = TestTemplate(model_name="test", model_manager=None)
    tmpl.render_header()

    # assert the title is correctly rendered
    assert markdown_mock.call_count == 1
    assert "My Test Template" in markdown_mock.call_args[0][0]


@pytest.mark.parametrize("display_name", [None, "New Title"])
@pytest.mark.parametrize("description", [None, "my description."])
def test_render_header_with_metadata(display_name, description, monkeypatch):
    metadata = {}
    if display_name:
        metadata["display_name"] = display_name
    if description:
        metadata["description"] = description
    markdown_mock = MagicMock()
    monkeypatch.setattr(st, "markdown", markdown_mock)
    tmpl = TestTemplate(model_name="test", model_manager=None, metadata=metadata)
    tmpl.render_header()

    assert markdown_mock.call_count == (2 if description else 1)
    expected_title = display_name if display_name else "My Test Template"
    assert expected_title in markdown_mock.call_args_list[0][0][0]
    if description:
        assert description in markdown_mock.call_args_list[1][0][0]


@pytest.mark.parametrize(
    "data",
    [
        ("str", "str", "abc", "abc", "xyz", "xyz"),
        ("int", "str", "1", 1, "1", "1"),
        ("int", "int", "1", 1, "1", 1),
        ("list", "str", "abc", ["abc"], "xyz", "xyz"),
        # if result is a non-empty batch, only return the first element
        ("list", "list", "abc", ["abc"], ["xyz"], "xyz"),
        ("", "list", "abc", ["abc"], ["xyz"], "xyz"),
        ("", "", "abc", ["abc"], ["xyz"], "xyz"),
        ("list", "", "abc", ["abc"], ["xyz"], "xyz"),
        ("typing.List", "typing.List", "abc", ["abc"], ["xyz"], "xyz"),
        ("typing.List[str]", "", "abc", ["abc"], ["xyz"], "xyz"),
        # if return is not a non-empty batch, return the data directly
        ("str", "str", "abc", "abc", ["xyz"], ["xyz"]),
        ("str", "list", "abc", "abc", ["xyz"], ["xyz"]),
        ("str", "", "abc", "abc", ["xyz"], ["xyz"]),
        ("str", "typing.List", "abc", "abc", ["xyz"], ["xyz"]),
        ("", "str", "abc", ["abc"], ["xyz"], ["xyz"]),
        ("list", "str", "abc", ["abc"], ["xyz"], ["xyz"]),
        ("list", "int", "abc", ["abc"], ["xyz"], ["xyz"]),
        ("list", "list", "abc", ["abc"], [], []),
        ("list", "list", "abc", ["abc"], "xyz", "xyz"),
        # fail to format
        ("str", "invalid-type", "abc", "abc", "xyz", "xyz"),
        ("invalid-type", "Lists", "abc", "abc", "xyz", "xyz"),
    ],
)
def test_auto_predict(data):
    input_type, output_type, raw_data, request_data, response_data, prediction = data
    metadata = {
        "input_type": input_type,
        "output_type": output_type,
    }

    tmpl = TestTemplate(model_name="test", model_manager=None, metadata=metadata)
    tmpl.render_header()

    tmpl.predict = MagicMock()
    tmpl.predict.return_value = response_data

    assert tmpl.auto_predict(raw_data) == prediction
    assert tmpl.predict.call_args[1]["data"] == request_data
