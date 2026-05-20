import allure
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    DEFAULT_TIMEOUT = 5

    def __init__(self, driver):
        self.driver = driver

    @allure.step("Открыть страницу: {url}")
    def open(self, url):
        self.driver.get(url)

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        return self.driver.current_url

    @allure.step("Проверить, что открыта страница: {url}")
    def is_url_opened(self, url):
        return self.get_current_url() == url

    def wait(self, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout)

    @allure.step("Найти элемент: {locator}")
    def find_element(self, locator):
        return self.driver.find_element(*locator)

    @allure.step("Найти элементы: {locator}")
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    @allure.step("Ввести текст в элемент: {locator}")
    def enter_text(self, locator, text, clear=True, timeout=DEFAULT_TIMEOUT):
        element = self.wait_for_element_visibility(locator, timeout)
        if clear:
            element.clear()
        element.send_keys(text)
        return element

    @allure.step("Очистить поле через Ctrl+A/Delete: {locator}")
    def clear_input(self, locator, timeout=DEFAULT_TIMEOUT):
        element = self.wait_for_element_visibility(locator, timeout)
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        return element

    @allure.step("Кликнуть по элементу: {locator}")
    def click_on_element(self, locator, timeout=DEFAULT_TIMEOUT):
        element = self.wait_for_element_to_be_clickable(locator, timeout)
        element.click()
        return element

    @allure.step("Прокрутить страницу к элементу: {locator}")
    def scroll_to_element(self, locator, timeout=DEFAULT_TIMEOUT):
        element = self.wait_for_element_visibility(locator, timeout)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element
        )
        return element

    @allure.step("Кликнуть JS по элементу: {locator}")
    def js_click_on_element(self, locator, timeout=DEFAULT_TIMEOUT):
        element = self.wait_for_element_visibility(locator, timeout)
        self.driver.execute_script("arguments[0].click();", element)
        return element

    @allure.step("Надежный клик по элементу: {locator}")
    def click_with_fallback(self, locator, timeout=DEFAULT_TIMEOUT):
        self.scroll_to_element(locator, timeout)
        try:
            return self.click_on_element(locator, timeout)
        except WebDriverException:
            return self.js_click_on_element(locator, timeout)

    @allure.step("Дождаться кликабельности элемента: {locator}")
    def wait_for_element_to_be_clickable(self, locator, timeout=DEFAULT_TIMEOUT):
        return self.wait(timeout).until(
            EC.element_to_be_clickable(locator),
            message=f"Элемент с локатором {locator} не кликабелен"
        )

    @allure.step("Дождаться видимости элемента: {locator}")
    def wait_for_element_visibility(self, locator, timeout=DEFAULT_TIMEOUT):
        return self.wait(timeout).until(
            EC.visibility_of_element_located(locator),
            message=f"Элемент с локатором {locator} не отображается"
        )

    @allure.step("Дождаться невидимости элемента: {locator}")
    def wait_for_element_invisibility(self, locator, timeout=DEFAULT_TIMEOUT):
        return self.wait(timeout).until(
            EC.invisibility_of_element_located(locator),
            message=f"Элемент с локатором {locator} всё ещё отображается"
        )

    @allure.step("Дождаться URL: {url}")
    def wait_for_url_to_be(self, url, timeout=DEFAULT_TIMEOUT):
        return self.wait(timeout).until(
            EC.url_to_be(url),
            message=f"Текущий URL не равен {url}"
        )

    @allure.step("Получить количество вкладок")
    def get_tabs_count(self):
        return len(self.driver.window_handles)

    @allure.step("Дождаться количества вкладок: {tabs_count}")
    def wait_for_tabs_count_to_be(self, tabs_count, timeout=DEFAULT_TIMEOUT):
        return self.wait(timeout).until(
            lambda driver: len(driver.window_handles) == tabs_count,
            message=f"Количество вкладок не равно {tabs_count}"
        )

    @allure.step("Переключиться на последнюю вкладку")
    def switch_to_last_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])
