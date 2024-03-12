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

driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[1]/button[2]').click()

driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[1]/button[2]').click()
time.sleep(1)

#간사이 국제 공항
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[10]/div[1]/div/input').send_keys('오사카')
time.sleep(1)
driver.find_element(By.XPATH, '//i[contains(text(), "간사이국제공항")]').click()
time.sleep(1)

driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[2]/button[1]').click()
time.sleep(1)

driver.find_elements(By.XPATH, '//b[text() = "16"]')[0].click()
time.sleep(1)

driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/button').click()
time.sleep(10)



# driver.find_element(By.XPATH, '').click()
# time.sleep(1)

# 전체 : indivisual_IndivisualItem__3co62 result
# 항공사 : airline_Airlines__8QpMj
# 출발 : route_Route__2UInh
# 가격 : item_defaultSummary__3hCaV

results = driver.find_elements(By.CLASS_NAME, 'indivisual_IndivisualItem__3co62.result')
for result in results:
    try:
        airline = result.find_element(By.CLASS_NAME, 'airline_Airlines__8QpMj').text
        startTime = result.find_element(By.CLASS_NAME, 'route_Route__2UInh').text
        price = result.find_element(By.CLASS_NAME, 'item_defaultSummary__3hCaV').text
        print(f'항공사 : {airline}')
        print(f'출발시간 : {startTime}')
        print(f'가격 : {price}')
    except:
        pass



input()