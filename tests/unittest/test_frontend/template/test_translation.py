from unittest.mock import MagicMock

from pinferencia.frontend.templates.translation import Template, TextToTextTemplate


def test_render(monkeypatch):
    render_mock = MagicMock()
    monkeypatch.setattr(TextToTextTemplate, "render", render_mock)

    tmpl = Template(model_name="test", model_manager=None)
    tmpl.render()

    assert render_mock.call_count == 1


def test_title():
    assert "trans" in Template.title.lower()
    assert "lation" in Template.title.lower()
