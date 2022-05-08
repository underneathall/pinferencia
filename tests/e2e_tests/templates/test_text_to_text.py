"""End to End Test For Text to Text Template"""

import pytest


@pytest.mark.parametrize("task", ["Text To Text", "Translation"])
def test_success(task, page):
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

    # fill the text area
    page.fill("textarea", "Hello.")
    main_div = page.locator("section.main")

    # click run button
    run_btn = main_div.locator("text=Run")
    run_btn.click()

    # wait for the result
    result = main_div.locator("text=abcdefg")
    result.wait_for(timeout=10000)

    assert result.count() == 1
