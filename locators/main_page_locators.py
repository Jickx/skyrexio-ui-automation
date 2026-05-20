from selenium.webdriver.common.by import By


class MainLocators:
    SUCCESS_TITLE = (
        By.XPATH,
        "//h1[contains(., 'Dashboard') or contains(., 'Welcome')]"
    )
