from unittest.mock import MagicMock, Mock

import pytest
from PIL import Image

from pinferencia.frontend.templates.image_to_image import Template, st


@pytest.mark.parametrize("upload", [True, False])
@pytest.mark.parametrize(
    "return_value_and_display_type",
    [
        (["use image_base64_string"], "image"),
    ],
)
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
    upload,
    return_value_and_display_type,
    metadata,
    image_base64_string,
    image_byte,
    monkeypatch,
):
    return_value, display_type = return_value_and_display_type
    if display_type == "image":
        return_value = [image_base64_string]

    # magic mock for general purpose mock
    st_mock = MagicMock()

    # mock the file uploader, return a byte object if upload is true
    file_uploader_mock = Mock(return_value=image_byte if upload else None)
    monkeypatch.setattr(st, "file_uploader", file_uploader_mock)

    # mock the upload form
    monkeypatch.setattr(st, "form", st_mock.form)
    monkeypatch.setattr(st, "form_submit_button", st_mock.form_submit_button)

    # mock the two columns
    col1_mock = MagicMock()
    col2_mock = MagicMock()
    mock_colums = Mock(return_value=(col1_mock, col2_mock))
    monkeypatch.setattr(st, "columns", mock_colums)

    # general purpose mock
    monkeypatch.setattr(st, "spinner", st_mock.spinner)

    # mock the model manager
    model_manager = MagicMock()
    model_manager.predict = Mock(return_value=return_value)

    # initialize and render the template
    tmpl = Template(model_name="test", metadata=metadata, model_manager=model_manager)
    tmpl.render()

    # assert file uploader is correctly called
    assert file_uploader_mock.call_count == 1
    assert file_uploader_mock.call_args[1]["type"] == ["jpg", "png", "jpeg"]

    # assert spinner is called if upload is true
    assert st_mock.spinner.call_count == (1 if upload else 0)

    # assert the correct method is called to display the result
    assert col2_mock.image.call_count == (1 if upload else 0)
    if col2_mock.image.called:
        call_arg = col2_mock.image.call_args[0][0]
        assert call_arg == Image.open(image_byte)

    # assert the model manager's predict is correctly called
    assert model_manager.predict.call_count == (1 if upload else 0)
    if model_manager.predict.called:
        assert (
            model_manager.predict.call_args[1]["data"] == [image_base64_string]
            if metadata.get("input_type") == "list"
            else image_base64_string
        )
        assert model_manager.predict.call_args[1]["model_name"] == "test"
        assert model_manager.predict.call_args[1]["version_name"] is None


def test_title():
    assert "image" in Template.title.lower()
    assert "text" not in Template.title.lower()
