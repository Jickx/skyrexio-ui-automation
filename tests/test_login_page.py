import allure
import pytest

from data.enums import LoginField
from data.login_cases import INVALID_PASSWORD_CASES
from pages.login_page import LoginPage


@allure.title("На странице логина есть поля Email и Password")
def test_login_page_has_email_and_password_fields(driver):
    login_page = LoginPage(driver)
    login_page.open_page()

    with allure.step("Проверить наличие поля Email"):
        assert login_page.has_field(LoginField.EMAIL)
    with allure.step("Проверить наличие поля Password"):
        assert login_page.has_field(LoginField.PASSWORD)


@allure.title("На странице логина есть кнопка Sign in")
def test_login_page_has_sign_in_button(driver):
    login_page = LoginPage(driver)
    login_page.open_page()

    with allure.step("Проверить наличие кнопки Sign in"):
        assert login_page.has_sign_in_button()


@allure.title("Проверка локализации страницы логина (RU/EN)")
@pytest.mark.parametrize(
    "browser_lang,expected_title,expected_subtitle,expected_button,expected_email_placeholder,expected_password_placeholder",
    [
        ("en-US", "Sign in", "Login to your account", "Sign in", "Email", "Password"),
        ("ru-RU", "Вход", "Войдите в свой аккаунт", "Войти", "Email", "Пароль"),
    ],
    ids=["english", "russian"],
    indirect=["browser_lang"]
)
def test_login_page_language_content(
    driver,
    browser_lang,
    expected_title,
    expected_subtitle,
    expected_button,
    expected_email_placeholder,
    expected_password_placeholder
):
    login_page = LoginPage(driver)
    login_page.open_page()

    with allure.step("Проверить заголовок страницы логина"):
        assert login_page.get_login_title() == expected_title
    with allure.step("Проверить подзаголовок страницы логина"):
        assert login_page.get_login_subtitle() == expected_subtitle
    with allure.step("Проверить текст кнопки входа"):
        assert login_page.get_sign_in_button_text() == expected_button
    with allure.step("Проверить placeholder поля Email"):
        assert login_page.get_email_placeholder() == expected_email_placeholder
    with allure.step("Проверить placeholder поля Password"):
        assert login_page.get_password_placeholder() == expected_password_placeholder


@allure.title("Рамка поля красная при невалидном вводе")
@pytest.mark.parametrize(
    "field,value",
    [
        (LoginField.EMAIL, "valentin.sh"),
        (LoginField.PASSWORD, "123"),
    ],
    ids=["invalid_email", "invalid_password"]
)
def test_field_border_is_red_for_invalid_value(driver, field, value):
    login_page = LoginPage(driver)
    login_page.open_page()

    if field == LoginField.EMAIL:
        login_page.enter_email(value)
    else:
        login_page.enter_password(value)
    login_page.blur_active_input()

    with allure.step(f"Проверить красную рамку у поля {field.value}"):
        assert login_page.is_field_border_red(field)


@allure.title("Рамка Password красная для набора невалидных паролей")
@pytest.mark.parametrize(
    "case_id,password",
    INVALID_PASSWORD_CASES,
    ids=[case[0] for case in INVALID_PASSWORD_CASES]
)
def test_password_border_is_red_for_invalid_password_cases(driver, case_id, password):
    login_page = LoginPage(driver)
    login_page.open_page()

    login_page.enter_password(password)
    login_page.blur_active_input()

    with allure.step(f"Проверить красную рамку Password для кейса: {case_id}"):
        assert login_page.is_field_border_red(LoginField.PASSWORD)
