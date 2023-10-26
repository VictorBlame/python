from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Edge()
driver.get('https://demo.seleniumeasy.com/jquery-download-progress-bar-demo.html')
driver.maximize_window()

button = driver.find_element(By.ID, 'downloadButton')
button.click()

try:
    progress = WebDriverWait(driver, 15).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "progress-label"), 'Complete!'))
    print(driver.find_element(By.CLASS_NAME, 'progress-label').text)

except:
    print('OH my')

finally:
    driver.close()
