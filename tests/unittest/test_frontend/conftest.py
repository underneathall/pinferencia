from unittest.mock import MagicMock, Mock

import pytest
import requests
import streamlit as st


@pytest.fixture
def clear_st_cache():
    try:
        # for version < 1.12.0
        st.legacy_caching.caching.clear_cache()
    except Exception:
        pass
    try:
        # for version >= 1.12.0
        st.runtime.legacy_caching.caching.clear_cache()
    except Exception:
        pass


@pytest.fixture
def requests_mock_model_abc_v1(monkeypatch):
    # mock requests.get
    response_mock = MagicMock()
    response_mock.status_code = 200
    response_mock.json = Mock(
        side_effect=[
            [{"name": "abc"}],
            [
                {"name": "v1"},
                {"name": "test-task", "task": "test"},
                {"name": "invalid-task", "task": "invalid-task"},
            ],
        ]
    )
    post_mock = Mock(return_value=response_mock)
    monkeypatch.setattr(requests, "get", post_mock)
