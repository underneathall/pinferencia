"""End to End Test For Custom Title and Description"""


def test_success(page):
    # choose the return text model
    model = page.locator("text=invalid-task-model")
    model.click()
    return_text_model = page.locator("text=custom-title-description")
    return_text_model.click()

    # fill the text area
    main_div = page.locator("section.main")

    title = main_div.locator("text='My Model'")
    title.wait_for(timeout=10000)

    assert title.count() == 1

    description = main_div.locator("text='This is my model.'")
    description.wait_for(timeout=10000)

    assert description.count() == 1
