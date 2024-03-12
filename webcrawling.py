from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
# from selenium.webdriver.common.by import
from selenium.webdriver.chrome.service import Service
import time

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get(url='https://flight.naver.com/')
time.sleep(5)

input()