from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

driver = webdriver.Edge()
driver.get('https://demo.seleniumeasy.com/basic-select-dropdown-demo.html')
driver.maximize_window()

chosen_day = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
day = chosen_day[3]

dropdown = Select(driver.find_element(By.ID, 'select-demo'))
dropdown.select_by_visible_text(day)

message = driver.find_element(By.CLASS_NAME, 'selected-value')
if message.text.replace('Day selected :- ', '') == day:
    print('Everything is okay')
else:
    print('HOUSTON!')


driver.close()
