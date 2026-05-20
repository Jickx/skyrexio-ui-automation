import allure

from pages.home_page import HomePage
from pages.login_page import LoginPage


@allure.title("Главная страница открывается")
def test_home_page_is_opened(driver):
    home_page = HomePage(driver)
    home_page.open_page()

    with allure.step("Проверить, что открылась главная страница"):
        assert home_page.is_opened()


@allure.title("На главной странице есть ссылка Login")
def test_home_page_has_login_link(driver):
    home_page = HomePage(driver)
    home_page.open_page()

    with allure.step("Проверить наличие ссылки Login"):
        assert home_page.has_login_link()


@allure.title("Переход на страницу логина по ссылке Login")
def test_open_login_page_from_home(driver):
    home_page = HomePage(driver)
    login_page = LoginPage(driver)

    home_page.open_page()
    home_page.click_login_link()

    with allure.step("Проверить, что открылась страница логина"):
        assert login_page.is_opened()


@allure.title("Возврат назад с login на home")
def test_back_navigation_from_login_to_home(driver):
    home_page = HomePage(driver)
    login_page = LoginPage(driver)

    home_page.open_page()
    login_page.open_page()
    driver.back()
    home_page.wait_until_opened()

    with allure.step("Проверить, что после Back открыта home страница"):
        assert home_page.is_opened()
