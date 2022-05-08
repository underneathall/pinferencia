from unittest.mock import MagicMock

from pinferencia.frontend.templates.image_style_transfer import (
    ImageToImageTemplate,
    Template,
)


def test_render(monkeypatch):
    render_mock = MagicMock()
    monkeypatch.setattr(ImageToImageTemplate, "render", render_mock)

    tmpl = Template(model_name="test", model_manager=None)
    tmpl.render()

    assert render_mock.call_count == 1


def test_title():
    assert "image" in Template.title.lower()
    assert "style" in Template.title.lower()
    assert "transfer" in Template.title.lower()
