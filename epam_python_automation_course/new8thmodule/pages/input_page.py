from base_page import BasePage
from new8thmodule.resources.locators import HomePageLocators


class InputPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get('https://demo.seleniumeasy.com/basic-first-form-demo.html')

    def add_text(self, search_text):
        self.enter_text(HomePageLocators.search_box, search_text)
        self.click(HomePageLocators.submit_button)

    def show_message(self, search_text):
        if HomePageLocators.message == search_text:
            print('Everything is fine')
        else:
            print('Something went wrong')