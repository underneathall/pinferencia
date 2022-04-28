from unittest.mock import MagicMock, Mock

import pytest

from pinferencia.frontend.templates.camera_image_to_text import Template, st


@pytest.mark.parametrize("click", [True, False])
@pytest.mark.parametrize(
    "return_value_and_display_type",
    [
        ("abc", "info"),
        (["abc"], "info"),
        ([[1, 2, 3]], "json"),
        ([[{"a": 1, "b": 2}, {"a": 3, "b": 4}]], "table"),
    ],
)
def test_render(
    click,
    return_value_and_display_type,
    image_base64_string,
    image_byte,
    monkeypatch,
):
    return_value, display_type = return_value_and_display_type

    # magic mock for general purpose mock
    st_mock = MagicMock()

    # mock the camera input, return a byte object if click is true
    camera_input_mock = Mock(return_value=image_byte if click else None)
    monkeypatch.setattr(st, "camera_input", camera_input_mock)

    # mock the two columns
    col_mock = MagicMock()
    mock_colums = Mock(return_value=(None, col_mock, None))
    monkeypatch.setattr(st, "columns", mock_colums)

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

    # assert file camera input is correctly called
    assert camera_input_mock.call_count == 1

    # assert spinner is called if click is true
    assert st_mock.spinner.call_count == (1 if click else 0)

    # assert the correct method is called to display the result
    for field in ("json", "info", "table"):
        module = getattr(col_mock, field)
        assert module.call_count == (1 if field == display_type and click else 0)
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
    assert model_manager.predict.call_count == (1 if click else 0)
    if model_manager.predict.called:
        assert model_manager.predict.call_args[1]["data"] == [image_base64_string]
        assert model_manager.predict.call_args[1]["model_name"] == "test"
        assert model_manager.predict.call_args[1]["version_name"] is None


def test_title():
    assert "camera" in Template.title.lower()
    assert "image" not in Template.title.lower()
    assert "text" in Template.title.lower()
