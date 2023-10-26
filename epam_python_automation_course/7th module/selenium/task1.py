from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Edge()
driver.get('https://demo.seleniumeasy.com/basic-first-form-demo.html')
driver.maximize_window()

searchtext = 'HOO'
searchbox = driver.find_element(By.ID, "user-message")
searchbox.send_keys(searchtext)

submit = driver.find_element(By.XPATH, "//button[text()='Show Message']")
submit.click()

message = driver.find_element(By.ID, "display")

if message.text == searchtext:
    print('Everything is fine')
else:
    print('Something went wrong')

driver.close()