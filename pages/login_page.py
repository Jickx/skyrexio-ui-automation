import allure
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from data.enums import LoginField
from pages.base_page import BasePage
from locators.login_page_locators import LoginLocators
from data.urls import Urls


class LoginPage(BasePage):
    POST_SUBMIT_TIMEOUT = 5
    RETRY_ON_CLEARED_FIELDS = 1

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

    @allure.step("Проверить наличие поля Email")
    def has_email_input(self):
        return self.wait_for_element_visibility(LoginLocators.EMAIL_INPUT, timeout=10).is_displayed()

    @allure.step("Проверить наличие поля Password")
    def has_password_input(self):
        return self.wait_for_element_visibility(LoginLocators.PASSWORD_INPUT, timeout=10).is_displayed()

    @allure.step("Проверить наличие кнопки Sign in")
    def has_sign_in_button(self):
        return self.wait_for_element_visibility(LoginLocators.SIGN_IN_BUTTON_ANY_LANG, timeout=10).is_displayed()

    @allure.step("Проверить наличие поля логина: {field}")
    def has_field(self, field: LoginField):
        locator = self.FIELD_LOCATORS[field]
        return self.wait_for_element_visibility(locator, timeout=10).is_displayed()

    @allure.step("Нажать кнопку Sign in")
    def click_sign_in(self):
        self.click_with_fallback(LoginLocators.SIGN_IN_BUTTON_ANY_LANG, timeout=10)

    @allure.step("Пауза для ручного нажатия Sign in")
    def wait_manual_sign_in(self):
        input("Нажмите Sign in в браузере вручную, затем нажмите Enter в консоли...")

    @allure.step("Отправить форму логина через fallback (Enter и JS submit)")
    def submit_login_fallback(self):
        password_input = self.wait_for_element_visibility(LoginLocators.PASSWORD_INPUT, timeout=10)
        password_input.send_keys(Keys.ENTER)

    @allure.step("Ожидать реакцию после Sign in")
    def wait_for_login_reaction(self, timeout=POST_SUBMIT_TIMEOUT):
        def login_reacted(driver):
            current_url = driver.current_url.rstrip("/")
            if current_url != Urls.LOGIN_URL.rstrip("/"):
                return True
            error_elements = driver.find_elements(*LoginLocators.ERROR_MESSAGE)
            return any(el.is_displayed() and el.text.strip() for el in error_elements)

        return self.wait(timeout).until(lambda driver: login_reacted(driver))

    @allure.step("Проверить, что поля логина очищены")
    def are_login_fields_cleared(self):
        email_value = self.find_element(LoginLocators.EMAIL_INPUT).get_attribute("value") or ""
        password_value = self.find_element(LoginLocators.PASSWORD_INPUT).get_attribute("value") or ""
        return email_value.strip() == "" and password_value.strip() == ""

    @allure.step("Снять фокус с активного поля")
    def blur_active_input(self):
        self.find_element((By.TAG_NAME, "body")).click()

    @allure.step("Проверить красную рамку Email")
    def is_email_border_red(self):
        classes = self.find_element(LoginLocators.EMAIL_INPUT_CONTAINER).get_attribute("class") or ""
        return "tw-border-red-500" in classes

    @allure.step("Проверить красную рамку Password")
    def is_password_border_red(self):
        classes = self.find_element(LoginLocators.PASSWORD_INPUT_CONTAINER).get_attribute("class") or ""
        return "tw-border-red-500" in classes

    @allure.step("Проверить красную рамку у поля: {field}")
    def is_field_border_red(self, field: LoginField):
        locator = self.FIELD_CONTAINER_LOCATORS[field]
        classes = self.find_element(locator).get_attribute("class") or ""
        return "tw-border-red-500" in classes

    @allure.step("Авторизоваться пользователем с email: {email}")
    def login(self, email, password, manual_submit=False):
        self.enter_email(email)
        self.enter_password(password)

        retries_left = self.RETRY_ON_CLEARED_FIELDS
        if manual_submit:
            self.wait_manual_sign_in()
        else:
            try:
                self.click_sign_in()
            except WebDriverException:
                self.submit_login_fallback()
            try:
                self.wait_for_login_reaction()
            except Exception:
                self.submit_login_fallback()

            while retries_left > 0 and self.is_opened() and self.are_login_fields_cleared():
                self.enter_email(email)
                self.enter_password(password)
                try:
                    self.click_sign_in()
                except WebDriverException:
                    self.submit_login_fallback()
                try:
                    self.wait_for_login_reaction()
                except Exception:
                    self.submit_login_fallback()
                retries_left -= 1

    @allure.step("Получить сообщение об ошибке")
    def get_error_message(self):
        return self.wait_for_element_visibility(
            LoginLocators.ERROR_MESSAGE
        ).text

    @allure.step("Получить заголовок страницы логина")
    def get_login_title(self):
        return self.wait_for_element_visibility(LoginLocators.LOGIN_TITLE, timeout=10).text.strip()

    @allure.step("Получить подзаголовок страницы логина")
    def get_login_subtitle(self):
        return self.wait_for_element_visibility(LoginLocators.LOGIN_SUBTITLE, timeout=10).text.strip()

    @allure.step("Получить текст кнопки входа")
    def get_sign_in_button_text(self):
        button = self.wait_for_element_visibility(LoginLocators.SIGN_IN_BUTTON_ANY_LANG, timeout=10)
        button_text = (button.text or "").strip()
        if button_text:
            return button_text
        value_text = (button.get_attribute("value") or "").strip()
        if value_text:
            return value_text
        return (button.get_attribute("aria-label") or "").strip()

    @allure.step("Получить placeholder поля Email")
    def get_email_placeholder(self):
        return (self.find_element(LoginLocators.EMAIL_INPUT).get_attribute("placeholder") or "").strip()

    @allure.step("Получить placeholder поля Password")
    def get_password_placeholder(self):
        return (self.find_element(LoginLocators.PASSWORD_INPUT).get_attribute("placeholder") or "").strip()
    FIELD_LOCATORS = {
        LoginField.EMAIL: LoginLocators.EMAIL_INPUT,
        LoginField.PASSWORD: LoginLocators.PASSWORD_INPUT,
    }

    FIELD_CONTAINER_LOCATORS = {
        LoginField.EMAIL: LoginLocators.EMAIL_INPUT_CONTAINER,
        LoginField.PASSWORD: LoginLocators.PASSWORD_INPUT_CONTAINER,
    }
