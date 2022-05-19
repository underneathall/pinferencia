from unittest.mock import MagicMock, Mock

import pytest

from pinferencia.frontend.templates.raw_request import Template, st


@pytest.mark.parametrize("clicked", [True, False])
@pytest.mark.parametrize(
    "return_value",
    [{"data": [1]}],
)
def test_render(clicked, return_value, monkeypatch):
    return_value = return_value

    # magic mock for general purpose mock
    st_mock = MagicMock()

    # mock the button
    button_mock = Mock(return_value=clicked)
    monkeypatch.setattr(st, "button", button_mock)

    # mock the two columns
    col1_mock = MagicMock()
    col2_mock = MagicMock()

    # mock the text area
    text_area_mock = Mock(return_value='{"data": ["a"]}')
    col1_mock.text_area = text_area_mock

    mock_colums = Mock(return_value=(col1_mock, col2_mock))
    monkeypatch.setattr(st, "columns", mock_colums)

    # general purpose mock
    monkeypatch.setattr(st, "spinner", st_mock.spinner)
    monkeypatch.setattr(st, "json", st_mock.json)

    # mock the model manager
    model_manager = MagicMock()
    model_manager.predict = Mock(return_value=return_value)

    # initialize and render the template
    tmpl = Template(model_name="test", model_manager=model_manager)
    tmpl.render()

    # assert the run button and text area are called
    assert button_mock.call_count == 1
    assert text_area_mock.call_count == 1
    assert col1_mock.text_area.call_count == 1
    assert col2_mock.json.call_count == 1

    # assert the correct method is called to display the result
    assert st_mock.spinner.call_count == (1 if clicked else 0)
    assert st_mock.json.call_count == (1 if clicked else 0)

    # assert the model manager's predict is correctly called
    assert model_manager.predict.call_count == (1 if clicked else 0)
    if model_manager.predict.called:
        assert model_manager.predict.call_args[1]["data"] == {"data": ["a"]}
        assert model_manager.predict.call_args[1]["model_name"] == "test"
        assert model_manager.predict.call_args[1]["version_name"] is None


def test_title():
    assert "raw" in Template.title.lower()
    assert "request" in Template.title.lower()
