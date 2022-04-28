from unittest.mock import Mock

from pinferencia.frontend.app import Server, st


def test_set_debug(requests_mock_model_abc_v1, clear_st_cache, monkeypatch):
    # mock the return value each time st.sidebar.selectbox is called
    # model_name, version_name, task
    selectbox_mock = Mock(side_effect=["abc", "v1", "text_to_text"])
    monkeypatch.setattr(st.sidebar, "selectbox", selectbox_mock)

    # mock st.warning
    mock_checkbox = Mock(return_value=True)
    monkeypatch.setattr(st.sidebar, "checkbox", mock_checkbox)

    service = Server(backend_server="http://127.0.0.1:8111")

    assert selectbox_mock.call_count == 3
    assert mock_checkbox.call_count == 1
    assert service.model_manager.api_manager.debug is True
