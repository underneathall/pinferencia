"""End to End Test For Text to Text Template"""

import pytest


@pytest.mark.parametrize("task", ["Text To Text", "Translation"])
@pytest.mark.parametrize("debug", [True, False])
def test_text_success(task, debug, page):
    # choose the return text model
    model = page.locator("text=invalid-task-model")
    model.click()
    return_text_model = page.locator("text=return-text-model")
    return_text_model.click()

    # locate the sidebar
    sidebar = page.locator('section[data-testid="stSidebar"]')

    # open the selector
    # here, instead of using:
    # task_selector = sidebar.locator(
    #     'div[data-baseweb="select"]:below(:text("Select the Task"))'
    # )
    # we choose to select the 'Text To Text' spefically, just in case
    # the task selection is clicked too fast and streamlit re-select the
    # default task of the model again.
    task_selector = sidebar.locator("text='Text To Text'")
    task_selector.click()

    # choose the task
    task = page.locator("li[role='option']").locator(f"text='{task}'")
    task.click()

    # enable debug
    if debug:
        sidebar.locator("text='Debug'").click()

    # fill the text area
    page.fill("textarea", "Hello.")
    main_div = page.locator("section.main")

    # click run button
    run_btn = main_div.locator("text=Run")
    run_btn.click()

    # wait for the result
    result = page.locator('div.stAlert:has-text("abcdefg")')
    result.wait_for(timeout=10000)

    assert result.count() == 1

    # wait for debug expander
    if debug:
        result = main_div.locator('div[data-testid="stExpander"]:has-text("Debug")')
        result.wait_for(timeout=10000)

        assert result.count() == 1


@pytest.mark.parametrize(
    "model_and_test_id",
    [
        ("return-json-model", "stJson"),
        ("return-table-model", "stTable"),
        ("return-invalid-table", "stJson"),
    ],
)
@pytest.mark.parametrize("task", ["Text To Text", "Translation"])
def test_json_table_success(model_and_test_id, task, page):
    model_name, test_id = model_and_test_id
    # choose the return text model
    model = page.locator("text=invalid-task-model")
    model.click()
    return_text_model = page.locator(f"text={model_name}")
    return_text_model.click()

    # locate the sidebar
    sidebar = page.locator('section[data-testid="stSidebar"]')

    # open the selector
    # here, instead of using:
    # task_selector = sidebar.locator(
    #     'div[data-baseweb="select"]:below(:text("Select the Task"))'
    # )
    # we choose to select the 'Text To Text' spefically, just in case
    # the task selection is clicked too fast and streamlit re-select the
    # default task of the model again.
    task_selector = sidebar.locator("text='Text To Text'")
    task_selector.click()

    # choose the task
    task = page.locator("li[role='option']").locator(f"text='{task}'")
    task.click()

    # fill the text area
    page.fill("textarea", "Hello.")
    main_div = page.locator("section.main")

    # click run button
    run_btn = main_div.locator("text=Run")
    run_btn.click()

    # wait for the result
    result = main_div.locator(f'div[data-testid="{test_id}"]:below(:text("Run"))')
    result.wait_for(timeout=10000)

    assert result.count() == 1
