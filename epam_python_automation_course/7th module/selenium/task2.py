from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def verifyButton(element, value):
    if element.get_attribute('value') == value:
        print("Everything is okay")
    else:
        print('Something went wrong. Value is: ' + button.get_attribute('value'))


driver = webdriver.Edge()
driver.get('https://demo.seleniumeasy.com/basic-checkbox-demo.html')
driver.maximize_window()

for chk in range(1, 5):
    option = 'Option ' + str(chk)
    check_box = driver.find_element(By.XPATH, "//label[text()[normalize-space()='" + option + "']]")
    check_box.click()

button = driver.find_element(By.ID, "check1")
verifyButton(button, 'Uncheck All')

check_box_1 = driver.find_element(By.XPATH, "//label[text()[normalize-space()='Option 1']]")
check_box_1.click()
verifyButton(button, 'Check All')

driver.close()
