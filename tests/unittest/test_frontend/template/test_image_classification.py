from unittest.mock import MagicMock

from pinferencia.frontend.templates.image_classification import (
    ImageToTextTemplate,
    Template,
)


def test_render(monkeypatch):
    render_mock = MagicMock()
    monkeypatch.setattr(ImageToTextTemplate, "render", render_mock)

    tmpl = Template(model_name="test", model_manager=None)
    tmpl.render()

    assert render_mock.call_count == 1


def test_title():
    assert "image" in Template.title.lower()
    assert "classification" in Template.title.lower()
