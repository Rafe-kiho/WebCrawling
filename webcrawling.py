import asyncio
import csv
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from datetime import datetime, timedelta

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless") # 헤드리스 모드 활성화
chrome_options.add_argument("--no-sandbox") # 샌드박스 사용 안 함
chrome_options.add_argument("--disable-dev-shm-usage") # /dev/shm 파티션 사용 안 함



# 국제선 27개 노선 * 2 -> 54개노선
route_international = [
    ["ICN", "KIX"], ["KIX", "ICN"],
    ["ICN", "NRT"], ["NRT", "ICN"],
    ["ICN", "HND"], ["HND", "ICN"],
    ["ICN", "OKA"], ["OKA", "ICN"],
    ["ICN", "FUK"], ["FUK", "ICN"],
    ["ICN", "CTS"], ["CTS", "ICN"],
    ["ICN", "NGO"], ["NGO", "ICN"],
    ["ICN", "DAD"], ["DAD", "ICN"],
    ["ICN", "CXR"], ["CXR", "ICN"],
    ["ICN", "SGN"], ["SGN", "ICN"],
    ["ICN", "HAN"], ["HAN", "ICN"],
    ["ICN", "PQC"], ["PQC", "ICN"],
    ["ICN", "BKK"], ["BKK", "ICN"],
    ["ICN", "HKT"], ["HKT", "ICN"],
    ["ICN", "LAX"], ["LAX", "ICN"],
    ["ICN", "HNL"], ["HNL", "ICN"],
    ["ICN", "JFK"], ["JFK", "ICN"],
    ["ICN", "SFO"], ["SFO", "ICN"],
    ["ICN", "SEA"], ["SEA", "ICN"],
    ["ICN", "ORD"], ["ORD", "ICN"],
    ["ICN", "LAS"], ["LAS", "ICN"],
    ["ICN", "IAD"], ["IAD", "ICN"],
    ["ICN", "ATL"], ["ATL", "ICN"],
    ["ICN", "EWR"], ["EWR", "ICN"],
    ["ICN", "CEB"], ["CEB", "ICN"],
    ["ICN", "MNL"], ["MNL", "ICN"],
    ["ICN", "CRK"], ["CRK", "ICN"],
]


async def parsing_async(airway_ID, departuredate, crawledHtml_li):
    # 로딩이 끝나면 생기는 비동기 elem : div.flights List domestic_DomesticFlight__3wvCd
    # 요소의 className -> CSS선택자로 추출
    # 전체 : div.indivisual_IndivisualItem__3co62 result
    # 항공사 : b.name -> CSS
    # 출발시간/도착시간 : route_time__-2Z1T[2]
    # 소요시간 : route_info__1RhUH 의 2번째 텍스트
    # 카드 혜택 : item_type__2KJOZ
    # 가격 : item_num__3R0Vz
    parsed_li = []
    for result in crawledHtml_li:
        try:
            airline = result.find(class_='airline_Airlines__8QpMj').text
            # 출발 시간 찾기
            departuretime = result.find(class_='route_Route__2UInh').text
            # 가격 정보 찾기
            price = result.find(class_='item_defaultSummary__3hCaV').text

            parsed_li.append([departuredate, airline, departuretime, price])


        # 요소에 데이터가 없는경우 패스
        except:
            pass
    return parsed_li


async def crawl_async(airway_ID, date, departuredate):
    global idx
    global currBrowser
    global countingURL
    global browserList

    departure = route_international[airway_ID][0]
    arrive = route_international[airway_ID][1]

    countingURL += 1
    url = (
        "https://m-flight.naver.com/flights/international/"
        + departure
        + "-"
        + arrive
        + "-"
        + date
        + "?adult=1&isDirect=true&fareType=Y"
    )
    # WebDriver에 Get요청 실패시 예외처리
    try:
        currBrowser.get(url)
    except:
        print("[ERROR] getUrl failed at ", departure, arrive, date)
        raise Exception("browser.get(url) Failed")
    # WebDriver를 이용한 비동기 html 로딩

    try:
        # 15초 이내 비동기 로딩 실패시 예외처리
        element = WebDriverWait(currBrowser, 20).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "flights.List.international_InternationalContainer__2sPtn")
            )
        )
    except:
        # webDriver 멈춤으로 인한 timeout
        idx = (idx + 1) % 4
        currBrowser = browserList[idx]
        print("[ERROR] 20s timeout at ", departure, arrive, date)
        print("[SYS] switching chrome browser to idx : ", idx)
        time.sleep(60)

        return list([])  # 재검색

    # bs4를 이용한 parsing

    soup = BeautifulSoup(currBrowser.page_source, "html.parser")
    crawledHtml_li = soup.select("div.indivisual_IndivisualItem__3co62.result")
    parsing_li = await parsing_async(airway_ID, departuredate, crawledHtml_li)  # bs4

    return parsing_li


async def main_async():
    global countingURL
    global datas_li
    global startTime

    global idx
    global currBrowser
    global countingURL
    global browserList

    countingURL = 0
    datas_li = []

    for airway_ID in range(len(route_international)):
        routeTotalFlights = 0
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        browser0 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # 브라우저 실행
        browser1 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # 브라우저 실행
        browser2 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # 브라우저 실행
        browser3 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # 브라우저 실행
        time.sleep(3)  # 브라우저 열고 잠깐 기다림
        browserList = [browser0, browser1, browser2, browser3]
        idx = 0
        currBrowser = browserList[idx]

        for days in range(1, 365):  # 1일뒤 항공편부터 존재(해외) 1년치
            # 90번마다 브라우저 리셋
            if days == 90:
                print("WebDriver Reload..")
                browser0.quit()
                time.sleep(3)

                options = webdriver.ChromeOptions()
                options.add_argument("headless")
                browser0 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # 브라우저 실행
                browser1 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # 브라우저 실행
                browser2 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # 브라우저 실행
                browser3 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # 브라우저 실행
                time.sleep(3)  # 브라우저 열고 잠깐 기다림
                browserList = [browser0, browser1, browser2, browser3]
                idx = 0
                currBrowser = browserList[idx]

            departure = route_international[airway_ID][0]
            arrive = route_international[airway_ID][1]
            searchedDate = (startTime + timedelta(days=days)).strftime("%Y%m%d")
            departuredate = (startTime + timedelta(days=days)).strftime("%Y.%m.%d %a")
            before_crawl_async = datetime.today()
            parsed_li = await crawl_async(airway_ID, searchedDate, departuredate)
            after_crawl_async = datetime.today()
            crawl_time = after_crawl_async - before_crawl_async
            print(
                f"{airway_ID}-{days}. {departure} to {arrive} at {searchedDate} have {len(parsed_li)} flights. Running Time : {crawl_time}(ms)"
            )

            print(parsed_li)

            routeTotalFlights += len(parsed_li)

            datas_li += parsed_li
        print(f">> {departure} to {arrive} flights : {routeTotalFlights}  --TOTAL FLIGHTS : {len(datas_li)}")
        print("----------------changing route----------------------\n")

        # 브라우저 리셋 - 끄기
        browser0.quit()

# main------------------------------------------------------------------------

global startTime
global idx
global currBrowser
global countingURL


# Running Time Check
startTime = datetime.today()

todayFileNameFormatting = startTime.strftime("%Y%m%d_%H%M%S")
print("today : ", todayFileNameFormatting)
print("20초 후 크롬드라이버 실행. 세션을 종료하세요")
time.sleep(20)


asyncio.run(main_async())

# Running Time Check
endTime = datetime.today()

print(f"[Start Time] {startTime}\n")
print(f"[End Time] {endTime}\n")
print(f"[Running Time] : { endTime - startTime} (ms)\n")
print(f"[File Length] {countingURL} url, {len(datas_li)} rows \n\n")

# csv 출력
# csv 파일 생성 및 데이터 쓰기
with open('crawling_results.csv', mode='w', newline='', encoding='utf-8') as fd:
    csvWriter = csv.writer(fd)
    # 컬럼 헤더 작성
    csvWriter.writerow(['날짜', '항공사', '출발시간', '가격'])
    # 크롤링 결과 작성
    csvWriter.writerows(datas_li)


# log 출력
log_fd = open("StormCrawler.txt", "a", newline="")
log_fd.write(f"[Start Time] {startTime}\n")
log_fd.write(f"[End Time] {endTime}\n")
log_fd.write(f"[Running Time] : { endTime - startTime} (ms)\n")
log_fd.write(f"[File Length] {countingURL} url, {len(datas_li)} rows \n\n")
log_fd.close()

print("[LOGGED] time log.txt generated")



#--------------------------------------------------------------------------------------------

# def wait_and_click(xpath):
#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
#
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#
# # 크롤링한 값 저장할 인덱스
# crawling_results = []
#
#
# # 네이버 항공권 접근
# driver.get(url='https://flight.naver.com/')
# time.sleep(3)
#
# wait_and_click('//*[@id="__next"]/div/div[1]/div[4]/div/div/div[1]/button[2]')  # 편도 선택
# wait_and_click('//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[1]/button[2]')  # 도착지 선택
#
# # 간사이 국제 공항
# driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[10]/div[1]/div/input').send_keys('오사카')
# time.sleep(1) # 로딩을 위한 대기
# wait_and_click('//i[contains(text(), "간사이국제공항")]')  # 간사이 국제 공항
# wait_and_click('//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[2]/button[1]')  # 도착지 확인
#
#
# # 출발 날짜 선택
# driver.find_elements(By.XPATH, '//b[text() = "16"]')[0].click()
# time.sleep(1) # 로딩을 위한 대기
#
# wait_and_click('//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[3]/button[2]')  # 직항만
#
# # 검색
# driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/button').click()
# time.sleep(10) # 로딩을 위한 대기
#
# # 날짜 데이터 가져오기
# wait_and_click('//*[@id="__next"]/div/div[1]/div[3]/div/div[2]/div/div[2]/em[1]/button')
# startDate = driver.find_element(By.CLASS_NAME, 'calendar_date__1T0wq').text
# wait_and_click('//*[@id="__next"]/div/div[2]/div[1]/button')
#
#
# # 항공권 결과 화면
# # 전체 : indivisual_IndivisualItem__3co62 result
# # 항공사 : airline_Airlines__8QpMj
# # 출발 : route_Route__2UInh
# # 가격 : item_defaultSummary__3hCaV
# results = driver.find_elements(By.CLASS_NAME, 'indivisual_IndivisualItem__3co62.result')
# for result in results:
#     try:
#         airline = result.find_element(By.CLASS_NAME, 'airline_Airlines__8QpMj').text
#         startTime = result.find_element(By.CLASS_NAME, 'route_Route__2UInh').text
#         price = result.find_element(By.CLASS_NAME, 'item_defaultSummary__3hCaV').text
#
#         # 확인용 출력
#         print(f'날짜 : {startDate}')
#         print(f'항공사 : {airline}')
#         print(f'출발시간 : {startTime}')
#         print(f'가격 : {price}')
#
#         # 결과를 리스트에 추가
#         crawling_results.append([startDate, airline, startTime, price])
#
#     except:
#         pass
#