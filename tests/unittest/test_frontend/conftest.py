from unittest.mock import MagicMock, Mock

import pytest
import requests
import streamlit as st


@pytest.fixture
def clear_st_cache():
    st.legacy_caching.caching.clear_cache()


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
