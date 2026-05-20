import allure

from data.urls import Urls
from locators.home_page_locators import HomeLocators
from pages.base_page import BasePage


class HomePage(BasePage):
    @allure.step("Открыть главную страницу")
    def open_page(self):
        self.open(Urls.BASE_URL)
        self.wait(timeout=10).until(
            lambda driver: "skyrexio.com" in driver.current_url,
            message="Не удалось открыть домен skyrexio.com"
        )

    @allure.step("Проверить, что открыта главная страница")
    def is_opened(self):
        return "skyrexio.com" in self.get_current_url()

    @allure.step("Дождаться открытия главной страницы")
    def wait_until_opened(self, timeout=10):
        return self.wait(timeout).until(
            lambda driver: "skyrexio.com" in driver.current_url and "/login" not in driver.current_url,
            message="Главная страница не открылась"
        )

    @allure.step("Проверить наличие ссылки Login")
    def has_login_link(self):
        return self.wait_for_element_visibility(HomeLocators.LOGIN_LINK, timeout=10).is_displayed()

    @allure.step("Перейти на страницу логина")
    def click_login_link(self):
        tabs_count = self.get_tabs_count()
        self.click_on_element(HomeLocators.LOGIN_LINK)
        self.wait_for_tabs_count_to_be(tabs_count + 1)
        self.switch_to_last_tab()
        self.wait_for_url_to_be(Urls.LOGIN_URL)
