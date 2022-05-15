"""End to End Test For Camera Image to Text Template"""

import time

import pytest
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError


@pytest.mark.parametrize("task", ["Camera Image To Image"])
def test_success(task, page):
    # choose the return text model
    model = page.locator("text=invalid-task-model")
    model.click()
    return_text_model = page.locator("text=return-image-model")
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
    task_selector = sidebar.locator("text='Text To Image'")
    task_selector.wait_for(timeout=10000)
    task_selector.click()

    # choose the task
    task = page.locator("li[role='option']").locator(f"text='{task}'")
    task.click()

    main_div = page.locator("section.main")

    # if the button is clicked too early, it will not work.
    # Even it is not disabled. Further experiments needed.
    # Currently a sleep and retry is used until a better solution
    # with element wait is found.
    time.sleep(1)

    for _ in range(10):
        page.click("text='Take Photo'")

        # wait for the result
        result = main_div.locator('div[data-testid="stImage"]:below(:text("Result"))')
        try:
            result.wait_for(timeout=5000)
            assert result.count() == 1
            break
        except PlaywrightTimeoutError:
            pass
        except Exception as exc:
            raise exc
    else:
        assert False
