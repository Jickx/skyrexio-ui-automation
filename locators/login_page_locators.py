from selenium.webdriver.common.by import By


class LoginLocators:
    LOGIN_LINK = (By.XPATH, "//*[text()='Login']")
    EMAIL_INPUT = (By.XPATH, "//input[@id='email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@id='password']")
    SIGN_IN_BUTTON = (By.XPATH, "//button[normalize-space()='Sign in']")
    SUCCESS_TITLE = (By.XPATH, "//h1[text()='Welcome to Skyrexio!']")
    ERROR_MESSAGE = (By.XPATH, "//*[contains(text(), 'Invalid') or contains(text(), 'required')]")
