from selenium.webdriver.common.by import By


class LoginLocators:
    EMAIL_INPUT = (By.XPATH, "//input[@id='email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@id='password']")
    SIGN_IN_BUTTON = (By.XPATH, "//button[@type='submit']")
    SIGN_IN_BUTTON_ANY_LANG = SIGN_IN_BUTTON
    LOGIN_TITLE = (By.XPATH, "//h1[normalize-space()='Sign in' or normalize-space()='Вход']")
    LOGIN_SUBTITLE = (By.XPATH, "//p[normalize-space()='Login to your account' or normalize-space()='Войдите в свой аккаунт']")
    EMAIL_INPUT_CONTAINER = (By.XPATH, "//input[@id='email']/ancestor::div[contains(@class,'tw-border')][1]")
    PASSWORD_INPUT_CONTAINER = (By.XPATH, "//input[@id='password']/ancestor::div[contains(@class,'tw-border')][1]")
    ERROR_MESSAGE = (By.XPATH, "//*[contains(text(), 'Invalid') or contains(text(), 'required')]")
