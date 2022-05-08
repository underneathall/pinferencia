"""End to End Test For Text to Text Template"""

import base64
import tempfile

import pytest


@pytest.mark.parametrize("task", ["Image To Text", "Image Classification"])
def test_success(task, image_base64_string, page):
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

    main_div = page.locator("section.main")

    # upload
    with page.expect_file_chooser() as fc_info:
        page.click("text='Browse files'")

    with tempfile.NamedTemporaryFile(mode="wb", suffix=".jpg") as f:
        # create a temporary image file and write the image bytes
        f.write(base64.b64decode(image_base64_string))

        # flush the content to disk
        f.flush()

        # choose the created file
        file_chooser = fc_info.value
        file_chooser.set_files(f.name)

        page.click("text='Upload and Run'")

        # wait for the result
        result = main_div.locator("text=abcdefg")
        result.wait_for(timeout=10000)

        assert result.count() == 1
