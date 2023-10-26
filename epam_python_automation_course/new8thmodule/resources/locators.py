from selenium.webdriver.common.by import By


class HomePageLocators():
    search_box = (By.ID, "user-message")
    submit_button = (By.XPATH, "//button[text()='Show Message']")
    message = (By.ID, "display")
