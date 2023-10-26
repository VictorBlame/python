from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Edge()
driver.get('https://demo.seleniumeasy.com/basic-radiobutton-demo.html')
driver.maximize_window()

sex_box = driver.find_element(By.XPATH, "(//input[@type='radio'])[3]")
age_box = driver.find_element(By.XPATH, "(//input[@name='ageGroup'])[2]")
get_values = driver.find_element(By.XPATH, "(//button[@class='btn btn-default'])[2]")
sex_box.click()
age_box.click()
get_values.click()


def attributeVerifier(element, options):
    for item in options:
        if item.replace(' ', '') == element.get_attribute('value'):
            print(element.get_attribute('value'))
            print('OKAY')


message = driver.find_element(By.CLASS_NAME, "groupradiobutton")

message_text = message.text.replace('\n', ':').replace(' ', '').split(':')
print(message_text)

attributeVerifier(sex_box, message_text)
attributeVerifier(age_box, message_text)

driver.close()
