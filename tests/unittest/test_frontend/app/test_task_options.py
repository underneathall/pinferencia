from unittest.mock import Mock

import pytest

from pinferencia.frontend.app import Server, st
from pinferencia.frontend.templates.base import BaseTemplate
from pinferencia.task import BUILT_IN_TASKS


@pytest.mark.parametrize("version_name", ["v1", "test-task", "invalid-task"])
def test_built_in_tasks(
    version_name, requests_mock_model_abc_v1, clear_st_cache, monkeypatch
):
    # mock the return value each time st.sidebar.selectbox is called
    # model_name, version_name, task
    selectbox_mock = Mock(side_effect=["abc", version_name, "text_to_text"])
    monkeypatch.setattr(st.sidebar, "selectbox", selectbox_mock)

    service = Server(backend_server="http://127.0.0.1:8111")

    assert selectbox_mock.call_count == 3
    supported_tasks_set = set(service.get_task_options())
    for task in BUILT_IN_TASKS:
        supported_tasks_set.remove(task)
    assert not supported_tasks_set


@pytest.mark.parametrize("version_name", ["v1", "test-task", "invalid-task"])
def test_custom_task_template(
    version_name,
    requests_mock_model_abc_v1,
    clear_st_cache,
    monkeypatch,
):
    # mock the return value each time st.sidebar.selectbox is called
    # model_name, version_name, task
    class TestTemplate(BaseTemplate):
        title = "My Test Template"

    selectbox_mock = Mock(side_effect=["abc", version_name, "test"])
    monkeypatch.setattr(st.sidebar, "selectbox", selectbox_mock)

    service = Server(
        backend_server="http://127.0.0.1:8111",
        custom_templates={"test": TestTemplate},
    )

    assert selectbox_mock.call_count == 3
    supported_tasks_set = set(service.get_task_options())
    for task in BUILT_IN_TASKS:
        supported_tasks_set.remove(task)
    supported_tasks_set.remove("test")
    assert not supported_tasks_set
