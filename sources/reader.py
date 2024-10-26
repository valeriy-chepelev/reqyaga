from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.get("https://pikabu.ru/")
WebDriverWait(driver=driver, timeout=20).until(
    lambda x: x.execute_script("return document.readyState === 'complete'"))
elements = driver.find_elements(By.CLASS_NAME, "story__title-link")
for element in elements:
    print(element.text)
