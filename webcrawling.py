import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time




def wait_and_click(xpath):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 크롤링한 값 저장할 인덱스
crawling_results = []

# 네이버 항공권 접근
driver.get(url='https://flight.naver.com/')
time.sleep(3)

wait_and_click('//*[@id="__next"]/div/div[1]/div[4]/div/div/div[1]/button[2]')  # 편도 선택
wait_and_click('//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[1]/button[2]')  # 도착지 선택

# 간사이 국제 공항
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[10]/div[1]/div/input').send_keys('오사카')
time.sleep(1) # 로딩을 위한 대기
wait_and_click('//i[contains(text(), "간사이국제공항")]')  # 간사이 국제 공항
wait_and_click('//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[2]/button[1]')  # 도착지 확인

# 출발 날짜 선택
driver.find_elements(By.XPATH, '//b[text() = "16"]')[0].click()
time.sleep(1) # 로딩을 위한 대기

wait_and_click('//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[3]/button[2]')  # 직항만

# 검색
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/button').click()
time.sleep(10) # 로딩을 위한 대기

# 날짜 데이터 가져오기
wait_and_click('//*[@id="__next"]/div/div[1]/div[3]/div/div[2]/div/div[2]/em[1]/button')
startDate = driver.find_element(By.CLASS_NAME, 'calendar_date__1T0wq').text
wait_and_click('//*[@id="__next"]/div/div[2]/div[1]/button')


# 항공권 결과 화면
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

        # 확인용 출력
        print(f'날짜 : {startDate}')
        print(f'항공사 : {airline}')
        print(f'출발시간 : {startTime}')
        print(f'가격 : {price}')

        # 결과를 리스트에 추가
        crawling_results.append([startDate, airline, startTime, price])

    except:
        pass

# CSV 파일 생성 및 데이터 쓰기
with open('crawling_results.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # 컬럼 헤더 작성
    writer.writerow(['날짜', '항공사', '출발시간', '가격'])
    # 크롤링 결과 작성
    writer.writerows(crawling_results)

# 사용자 입력 대기
input("Press Enter to continue...")
