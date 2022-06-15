from unittest.mock import MagicMock, Mock

import pytest
from PIL import Image

from pinferencia.frontend.templates.text_to_image import Template, st


@pytest.mark.parametrize("clicked", [True, False])
@pytest.mark.parametrize(
    "metadata",
    [
        {},
        {"input_type": "str"},
        {"output_type": "str"},
        {"input_type": "list", "output_type": "str"},
        {"input_type": "str", "output_type": "list"},
    ],
)
def test_render(
    clicked,
    metadata,
    image_base64_string,
    image_byte,
    monkeypatch,
):
    # magic mock for general purpose mock
    st_mock = MagicMock()

    # mock the button
    button_mock = Mock(return_value=clicked)
    monkeypatch.setattr(st, "button", button_mock)

    # mock the text area
    text_input_mock = Mock(return_value="abcdefg")
    monkeypatch.setattr(st, "text_input", text_input_mock)

    # general purpose mock
    monkeypatch.setattr(st, "spinner", st_mock.spinner)
    monkeypatch.setattr(st, "image", st_mock.image)

    # mock the model manager
    model_manager = MagicMock()
    model_manager.predict = Mock(return_value=[image_base64_string])

    # initialize and render the template
    tmpl = Template(model_name="test", metadata=metadata, model_manager=model_manager)
    tmpl.render()

    # assert the run button and text area are called
    assert button_mock.call_count == 1
    assert text_input_mock.call_count == 1

    # assert the correct method is called to display the result
    assert st_mock.spinner.call_count == (1 if clicked else 0)
    assert st_mock.image.call_count == (1 if clicked else 0)
    if st_mock.image.called:
        assert st_mock.image.call_args[0][0] == Image.open(image_byte)

    # assert the model manager's predict is correctly called
    assert model_manager.predict.call_count == (1 if clicked else 0)
    if model_manager.predict.called:
        assert (
            model_manager.predict.call_args[1]["data"] == ["abcdefg"]
            if metadata.get("input_type") == "list"
            else "abcdefg"
        )
        assert model_manager.predict.call_args[1]["model_name"] == "test"
        assert model_manager.predict.call_args[1]["version_name"] is None


def test_title():
    assert "image" in Template.title.lower()
    assert "text" in Template.title.lower()
