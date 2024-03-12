from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
# from selenium.webdriver.common.by import
from selenium.webdriver.chrome.service import Service
import time

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get(url='https://flight.naver.com/')
time.sleep(3)

driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[1]/button[2]').click()
time.sleep(1)

#간사이 국제 공항
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[10]/div[1]/div/input').send_keys('오사카')
time.sleep(1)
driver.find_element(By.XPATH, '//i[contains(text(), "간사이국제공항")]').click()
time.sleep(1)

# driver.find_element(By.XPATH, '').click()
# time.sleep(1)



input()