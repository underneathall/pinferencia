"""End to End Test For Large Result Template"""


def test_success(page):
    # choose the return text model
    model = page.locator("text=invalid-task-model")
    model.click()
    return_text_model = page.locator("text=return-large-result")
    return_text_model.click()

    # locate the sidebar
    sidebar = page.locator('section[data-testid="stSidebar"]')

    # enable debug
    sidebar.locator("text='Debug'").click()

    # fill the text area
    page.fill("textarea", "Hello.")
    main_div = page.locator("section.main")

    # click run button
    run_btn = main_div.locator("text=Run")
    run_btn.click()

    debug_expander = main_div.locator('div[data-testid="stExpander"]:has-text("Debug")')
    debug_expander.click()

    # wait for the result
    warning_message = main_div.locator('text="The JSON body is too large to display."')
    warning_message.wait_for(timeout=10000)
    assert warning_message.count() == 1

    display_result = debug_expander.locator("div.stMarkdown").locator("code")
    display_result.wait_for(timeout=10000)
    assert display_result.count() == 1
