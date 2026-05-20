import allure

from data.urls import Urls
from locators.home_page_locators import HomeLocators
from pages.base_page import BasePage


class HomePage(BasePage):
    @allure.step("Открыть главную страницу")
    def open_page(self):
        self.open(Urls.HOME_URL)
        self.wait_for_url_to_be(Urls.HOME_URL)

    @allure.step("Проверить, что открыта главная страница")
    def is_opened(self):
        return self.is_url_opened(Urls.HOME_URL)

    @allure.step("Перейти на страницу логина")
    def click_login_link(self):
        tabs_count = self.get_tabs_count()
        self.click_on_element(HomeLocators.LOGIN_LINK)
        self.wait_for_tabs_count_to_be(tabs_count + 1)
        self.switch_to_last_tab()
        self.wait_for_url_to_be(Urls.LOGIN_URL)
