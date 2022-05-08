from unittest.mock import MagicMock

import pytest

from pinferencia.frontend.app import Server, st
from pinferencia.frontend.config import DEFAULT_DETAIL_DESCRIPTION


@pytest.mark.parametrize("title", [None, "abc"])
def test_title(title, requests_mock_model_abc_v1, clear_st_cache, monkeypatch):
    # mock sidebar title function
    title_mock = MagicMock()
    monkeypatch.setattr(st.sidebar, "title", title_mock)

    service = Server(backend_server="http://127.0.0.1:8111", title=title)
    assert service.title == title if title else "Pinferencia"
    assert title_mock.call_args_list[0][0][0] == title if title else "Pinferencia"


@pytest.mark.parametrize("short_description", [None, "abc"])
def test_short_description(
    short_description, requests_mock_model_abc_v1, clear_st_cache, monkeypatch
):
    # mock sidebar markdown function
    markdown_mock = MagicMock()
    monkeypatch.setattr(st.sidebar, "markdown", markdown_mock)

    kwargs = {"backend_server": "http://127.0.0.1:8111"}
    if short_description:
        kwargs["short_description"] = short_description
    service = Server(**kwargs)

    # assert the method is called correctly
    if short_description:
        assert service.short_description == short_description
        assert markdown_mock.call_args_list[0][0][0] == short_description
    else:
        assert (
            "[GitHub](https://github.com/underneathall/pinferencia) | "
            "[Documentation](https://pinferencia.underneathall.app)"
        ) == markdown_mock.call_args_list[0][0][0]


@pytest.mark.parametrize("detail_description", [None, "abc"])
def test_detail_description(
    detail_description, requests_mock_model_abc_v1, clear_st_cache, monkeypatch
):
    # mock sidebar set_page_config function
    set_page_config_mock = MagicMock()
    monkeypatch.setattr(st, "set_page_config", set_page_config_mock)

    kwargs = {"backend_server": "http://127.0.0.1:8111"}
    if detail_description:
        kwargs["detail_description"] = detail_description
    service = Server(**kwargs)

    # assert the method is called correctly
    if detail_description:
        assert service.detail_description == detail_description
        assert (
            set_page_config_mock.call_args_list[0][1]["menu_items"]["About"]
            == detail_description
        )
    else:
        assert (
            set_page_config_mock.call_args_list[0][1]["menu_items"]["About"]
            == DEFAULT_DETAIL_DESCRIPTION
        )
