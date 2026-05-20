import allure
import pytest
from selenium import webdriver
from allure_commons.types import AttachmentType


@pytest.fixture(scope="function")
def driver():
    with allure.step("Запустить браузер Chrome"):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()

    yield driver

    with allure.step("Закрыть браузер"):
        driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or report.passed:
        return

    driver = item.funcargs.get("driver")
    if not driver:
        return

    allure.attach(
        driver.get_screenshot_as_png(),
        name="failure_screenshot",
        attachment_type=AttachmentType.PNG
    )

    browser_logs = driver.get_log("browser")
    if browser_logs:
        formatted_logs = "\n".join(
            f"[{entry.get('level', 'INFO')}] {entry.get('message', '')}"
            for entry in browser_logs
        )
        allure.attach(
            formatted_logs,
            name="browser_console_logs",
            attachment_type=AttachmentType.TEXT
        )
