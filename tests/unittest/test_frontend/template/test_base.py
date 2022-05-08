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
