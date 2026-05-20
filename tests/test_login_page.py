import time

import allure

from pages.login_page import LoginPage
from pages.main_page import MainPage
from data.user_factory import UserFactory


@allure.title("Авторизация валидного пользователя")
def test_login_valid_user(driver):
    user = UserFactory.valid_user()
    login_page = LoginPage(driver)
    main_page = MainPage(driver)
    login_page.open_page()
    with allure.step("Проверить, что открылась страница логина"):
        assert login_page.is_opened()
    login_page.login(user["email"], user["password"])
    with allure.step("Проверить успешную авторизацию"):
        assert main_page.is_opened(), main_page.get_open_state_details()


@allure.title("Авторизация с невалидными учетными данными")
def test_login_invalid_user(driver):
    user = UserFactory.invalid_user()
    login_page = LoginPage(driver)
    login_page.open_page()
    with allure.step("Проверить, что открылась страница логина"):
        assert login_page.is_opened()
    login_page.login(user["email"], user["password"])
    with allure.step("Проверить сообщение об ошибке авторизации"):
        assert "Invalid email or password" in login_page.get_error_message()


@allure.title("Валидация поля email на странице логина")
def test_login_email_validation(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    with allure.step("Проверить, что открылась страница логина"):
        assert login_page.is_opened()
    user = UserFactory.invalid_email_user()
    login_page.login(user["email"], user["password"])
    with allure.step("Проверить ошибку для некорректного email"):
        assert "Invalid email" in login_page.get_error_message()
    user = UserFactory.empty_email_user()
    login_page.login(user["email"], user["password"])
    with allure.step("Проверить ошибку для пустого email"):
        assert "Email is required" in login_page.get_error_message()


@allure.title("Валидация поля password на странице логина")
def test_login_password_validation(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    with allure.step("Проверить, что открылась страница логина"):
        assert login_page.is_opened()
    user = UserFactory.empty_password_user()
    login_page.login(user["email"], user["password"])
    with allure.step("Проверить ошибку для пустого пароля"):
        assert "Password is required" in login_page.get_error_message()
