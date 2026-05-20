import allure

from pages.base_page import BasePage
from locators.login_page_locators import LoginLocators
from data.urls import Urls


class LoginPage(BasePage):
    @allure.step("Открыть страницу логина")
    def open_page(self):
        self.open(Urls.LOGIN_URL)
        self.wait_for_url_to_be(Urls.LOGIN_URL)

    @allure.step("Проверить, что открыта страница логина")
    def is_opened(self):
        return self.is_url_opened(Urls.LOGIN_URL)

    @allure.step("Ввести email: {email}")
    def enter_email(self, email):
        self.enter_text(LoginLocators.EMAIL_INPUT, email)

    @allure.step("Ввести пароль")
    def enter_password(self, password):
        self.enter_text(LoginLocators.PASSWORD_INPUT, password)

    @allure.step("Нажать кнопку Sign in")
    def click_sign_in(self):
        self.click_with_fallback(LoginLocators.SIGN_IN_BUTTON, timeout=10)

    @allure.step("Пауза для ручного нажатия Sign in")
    def wait_manual_sign_in(self):
        input("Нажмите Sign in в браузере вручную, затем нажмите Enter в консоли...")

    @allure.step("Авторизоваться пользователем с email: {email}")
    def login(self, email, password, manual_submit=False):
        self.enter_email(email)
        self.enter_password(password)
        if manual_submit:
            self.wait_manual_sign_in()
        else:
            self.click_sign_in()

    @allure.step("Получить сообщение об ошибке")
    def get_error_message(self):
        return self.wait_for_element_visibility(
            LoginLocators.ERROR_MESSAGE
        ).text
