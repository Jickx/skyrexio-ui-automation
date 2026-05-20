from selenium.webdriver.common.by import By


class MainLocators:
    # В интерфейсе текст может меняться, поэтому используем несколько сигналов
    SUCCESS_TITLE = (
        By.XPATH,
        "//h1[contains(., 'Dashboard') or contains(., 'Welcome')]"
    )
