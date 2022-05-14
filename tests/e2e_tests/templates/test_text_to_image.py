"""End to End Test For Text to Text Template"""

import pytest


@pytest.mark.parametrize("task", ["Text To Image"])
def test_success(task, page):
    # choose the return text model
    model = page.locator("text=invalid-task-model")
    model.click()
    return_image_model = page.locator("text=return-image-model")
    return_image_model.click()

    # fill the text area
    main_div = page.locator("section.main")
    text_input = main_div.locator("input")
    text_input.fill("cup")

    # click run button
    run_btn = main_div.locator("text=Run")
    run_btn.click()

    # wait for the result
    result = main_div.locator('div[data-testid="stImage"]:below(:text("Run"))')
    result.wait_for(timeout=10000)

    assert result.count() == 1
