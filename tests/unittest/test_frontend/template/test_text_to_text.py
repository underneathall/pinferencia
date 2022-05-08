from unittest.mock import MagicMock, Mock

import pytest

from pinferencia.frontend.templates.text_to_text import Template, st


@pytest.mark.parametrize("clicked", [True, False])
@pytest.mark.parametrize(
    "return_value_and_display_type",
    [
        ("abc", "info"),
        (["abc"], "info"),
        ([[1, 2, 3]], "json"),
        ([[{"a": 1, "b": 2}, {"a": 3, "b": 4}]], "table"),
    ],
)
def test_render(clicked, return_value_and_display_type, monkeypatch):
    return_value, display_type = return_value_and_display_type

    # magic mock for general purpose mock
    st_mock = MagicMock()

    # mock the button
    button_mock = Mock(return_value=clicked)
    monkeypatch.setattr(st, "button", button_mock)

    # mock the text area
    text_area_mock = Mock(return_value="abcdefg")
    monkeypatch.setattr(st, "text_area", text_area_mock)

    # general purpose mock
    monkeypatch.setattr(st, "spinner", st_mock.spinner)
    monkeypatch.setattr(st, "json", st_mock.json)
    monkeypatch.setattr(st, "info", st_mock.info)
    monkeypatch.setattr(st, "table", st_mock.table)

    # mock the model manager
    model_manager = MagicMock()
    model_manager.predict = Mock(return_value=return_value)

    # initialize and render the template
    tmpl = Template(model_name="test", model_manager=model_manager)
    tmpl.render()

    # assert the run button and text area are called
    assert button_mock.call_count == 1
    assert text_area_mock.call_count == 1

    # assert the correct method is called to display the result
    assert st_mock.spinner.call_count == (1 if clicked else 0)
    for field in ("json", "info", "table"):
        module = getattr(st_mock, field)
        assert module.call_count == (1 if field == display_type and clicked else 0)
        if module.called:
            call_arg = module.call_args[0][0]
            if field == "table":
                call_arg = call_arg.to_dict("records")
            assert (
                call_arg == return_value[0]
                if isinstance(return_value, list)
                else return_value
            )

    # assert the model manager's predict is correctly called
    assert model_manager.predict.call_count == (1 if clicked else 0)
    if model_manager.predict.called:
        assert model_manager.predict.call_args[1]["data"] == ["abcdefg"]
        assert model_manager.predict.call_args[1]["model_name"] == "test"
        assert model_manager.predict.call_args[1]["version_name"] is None


def test_title():
    assert "image" not in Template.title.lower()
    assert "text" in Template.title.lower()
