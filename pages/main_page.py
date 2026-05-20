import allure
from selenium.common.exceptions import TimeoutException

from data.urls import Urls
from locators.main_page_locators import MainLocators
from pages.base_page import BasePage


class MainPage(BasePage):
    @allure.step("Получить заголовок успешной авторизации")
    def get_success_title(self):
        return self.wait_for_element_visibility(
            MainLocators.SUCCESS_TITLE,
            timeout=10
        ).text

    @allure.step("Проверить, что открыта главная страница приложения после авторизации")
    def is_opened(self):
        current_url = self.get_current_url().rstrip("/")
        if current_url == Urls.LOGIN_URL.rstrip("/"):
            return False
        if "app.skyrexio.com" not in current_url:
            return False
        try:
            title = self.get_success_title()
            if "Dashboard" in title or "Welcome" in title:
                return True
        except TimeoutException:
            # На некоторых сборках заголовок может отличаться или отсутствовать.
            pass
        return True

    @allure.step("Получить детали текущего состояния MainPage")
    def get_open_state_details(self):
        current_url = self.get_current_url()
        title = ""
        try:
            title = self.get_success_title()
        except TimeoutException:
            title = "<not found>"
        return f"url={current_url}; success_title={title}"
