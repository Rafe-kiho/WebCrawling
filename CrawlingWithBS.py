# import csv
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium import webdriver  # 외부
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from bs4 import BeautifulSoup
#
# from datetime import datetime, timedelta
# import time
#
# import asyncio  # 외부
# import logging  # 미사용?
#
# from webdriver_manager.chrome import ChromeDriverManager
#
#
# chrome_options = webdriver.ChromeOptions()
#
# # 국제선 27개 노선 * 2 -> 54개노선 -> 18개
# route_international = [
#     ["ICN", "KIX"], ["KIX", "ICN"],
#     ["ICN", "NRT"], ["NRT", "ICN"],
#     ["ICN", "HND"], ["HND", "ICN"],
#     ["ICN", "OKA"], ["OKA", "ICN"],
#     ["ICN", "FUK"], ["FUK", "ICN"],
#     ["ICN", "CTS"], ["CTS", "ICN"],
#     ["ICN", "NGO"], ["NGO", "ICN"],
#     ["ICN", "DAD"], ["DAD", "ICN"],
#     ["ICN", "CXR"], ["CXR", "ICN"],
#     ["ICN", "SGN"], ["SGN", "ICN"],
#     ["ICN", "HAN"], ["HAN", "ICN"],
#     ["ICN", "PQC"], ["PQC", "ICN"],
#     ["ICN", "BKK"], ["BKK", "ICN"],
#     ["ICN", "HKT"], ["HKT", "ICN"],
#     ["ICN", "LAX"], ["LAX", "ICN"],
#     ["ICN", "HNL"], ["HNL", "ICN"],
#     ["ICN", "JFK"], ["JFK", "ICN"],
#     ["ICN", "SFO"], ["SFO", "ICN"],
#     ["ICN", "SEA"], ["SEA", "ICN"],
#     ["ICN", "ORD"], ["ORD", "ICN"],
#     ["ICN", "LAS"], ["LAS", "ICN"],
#     ["ICN", "IAD"], ["IAD", "ICN"],
#     ["ICN", "ATL"], ["ATL", "ICN"],
#     ["ICN", "EWR"], ["EWR", "ICN"],
#     ["ICN", "CEB"], ["CEB", "ICN"],
#     ["ICN", "MNL"], ["MNL", "ICN"],
#     ["ICN", "CRK"], ["CRK", "ICN"],
# ]
#
# async def parsing_async(airway_ID, date, crawledHtml_li):
#     # 로딩이 끝나면 생기는 비동기 elem : div.flights List domestic_DomesticFlight__3wvCd
#     # 요소의 className -> CSS선택자로 추출
#     # 전체 : div.indivisual_IndivisualItem__3co62 result
#     # 항공사 : b.name -> CSS
#     # 출발시간/도착시간 : route_time__-2Z1T[2]
#     # 소요시간 : route_info__1RhUH 의 2번째 텍스트
#     # 카드 혜택 : item_type__2KJOZ
#     # 가격 : item_num__3R0Vz
#     parsed_li = []
#     for elem in crawledHtml_li:
#         try:
#
#             airline = elem.find(class_='airline_Airlines__8QpMj').get_text()
#             starttime = elem.find(class_='route_Route__2UInh').get_text()
#             price = elem.find(class_='item_defaultSummary__3hCaV').get_text()
#
#             parsed_li.append([date, airline, starttime, price, airway_ID])
#
#
#         # 요소에 데이터가 없는경우 패스
#         except:
#             pass
#     return parsed_li
#
#
# async def crawl_async(airway_ID, date):
#     global idx
#     global currBrowser
#     global countingURL
#     global browserList
#
#     departure = route_international[airway_ID][0]
#     arrive = route_international[airway_ID][1]
#
#     countingURL += 1
#     url = (
#         "https://m-flight.naver.com/flights/international/"
#         + departure
#         + "-"
#         + arrive
#         + "-"
#         + date
#         + "?adult=1&isDirect=true&fareType=Y"
#     )
#     # WebDriver에 Get요청 실패시 예외처리
#     try:
#         currBrowser.get(url)
#     except:
#         print("[ERROR] getUrl failed at ", departure, arrive, date)
#         raise Exception("browser.get(url) Failed")
#     # WebDriver를 이용한 비동기 html 로딩
#
#     try:
#         # 15초 이내 비동기 로딩 실패시 예외처리
#         element = WebDriverWait(currBrowser, 20).until(
#             EC.presence_of_element_located(
#                 (By.CLASS_NAME, "flights.List.international_InternationalContainer__2sPtn")
#             )
#         )
#     except:
#         # webDriver 멈춤으로 인한 timeout
#         idx = (idx + 1) % 4
#         currBrowser = browserList[idx]
#         print("[ERROR] 20s timeout at ", departure, arrive, date)
#         print("[SYS] switching chrome browser to idx : ", idx)
#         time.sleep(60)
#
#         return list([])  # 재검색
#
#     # bs4를 이용한 parsing
#
#     soup = BeautifulSoup(currBrowser.page_source, "html.parser")
#     crawledHtml_li = soup.find_all("div", class_="indivisual_IndivisualItem__3co62.result")
#     parsing_li = await parsing_async(airway_ID, date, crawledHtml_li)  # bs4
#
#     return parsing_li
#
#
# async def main_async():
#     global countingURL
#     global datas_li
#     global startTime
#
#     global idx
#     global currBrowser
#     global countingURL
#     global browserList
#
#     countingURL = 0
#     datas_li = []
#
#     for airway_ID in range(len(route_international)):
#         routeTotalFlights = 0
#         options = webdriver.ChromeOptions()
#         options.add_argument("headless")
#         browser0 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # 브라우저 실행
#         browser1 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # 브라우저 실행
#         browser2 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # 브라우저 실행
#         browser3 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # 브라우저 실행
#         time.sleep(3)  # 브라우저 열고 잠깐 기다림
#         browserList = [browser0, browser1, browser2, browser3]
#         idx = 0
#         currBrowser = browserList[idx]
#
#         for days in range(1, 365):  # 3일뒤 항공편부터 존재(해외) 6개월까지
#             # 90번마다 브라우저 리셋
#             if days == 90:
#                 print("WebDriver Reload..")
#                 browser0.quit()
#                 browser1.quit()
#                 browser2.quit()
#                 browser3.quit()
#                 time.sleep(3)
#
#                 options = webdriver.ChromeOptions()
#                 options.add_argument("headless")
#                 browser0 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # 브라우저 실행
#                 browser1 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # 브라우저 실행
#                 browser2 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # 브라우저 실행
#                 browser3 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # 브라우저 실행
#                 time.sleep(3)  # 브라우저 열고 잠깐 기다림
#                 browserList = [browser0, browser1, browser2, browser3]
#                 idx = 0
#                 currBrowser = browserList[idx]
#
#             departure = route_international[airway_ID][0]
#             arrive = route_international[airway_ID][1]
#             searchedDate = (startTime + timedelta(days=days)).strftime("%Y%m%d")
#             before_crawl_async = datetime.today() + timedelta(hours=9)
#             parsed_li = await crawl_async(airway_ID, searchedDate)
#             after_crawl_async = datetime.today() + timedelta(hours=9)
#             crawl_time = after_crawl_async - before_crawl_async
#             print(
#                 f"{airway_ID}-{days}. {departure} to {arrive} at {searchedDate} have {len(parsed_li)} flights. Running Time : {crawl_time}(ms)"
#             )
#
#             print(parsed_li)
#
#             routeTotalFlights += len(parsed_li)
#
#             datas_li += parsed_li
#         print(f">> {departure} to {arrive} flights : {routeTotalFlights}  --TOTAL FLIGHTS : {len(datas_li)}")
#         print("----------------changing route----------------------\n")
#
#         # 브라우저 리셋 - 끄기
#         browser0.quit()
#         browser1.quit()
#         browser2.quit()
#         browser3.quit()
#
#     # Flight Ticket ID, searchingDate 후처리
#     for i in range(len(datas_li)):
#         datas_li[i][0] = i
#         datas_li[i][1] = startTime.strftime("%Y-%m-%d")
#
#
# # main------------------------------------------------------------------------
#
# global startTime
# global idx
# global currBrowser
# global countingURL
#
# # Running Time Check
# startTime = datetime.today() + timedelta(hours=9)
#
# todayFileNameFormatting = startTime.strftime("%Y%m%d_%H%M%S")
# print("today : ", todayFileNameFormatting)
# print("20초 후 크롬드라이버 실행. 세션을 종료하세요")
# time.sleep(20)
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main_async())  # 비동기
# loop.close()
#
# # Running Time Check
# endTime = datetime.today() + timedelta(hours=9)
#
# print(f"[Start Time] {startTime}\n")
# print(f"[End Time] {endTime}\n")
# print(f"[Running Time] : { endTime - startTime} (ms)\n")
# print(f"[File Length] {countingURL} url, {len(datas_li)} rows \n\n")
#
# # csv 출력
# fd = open(f"{todayFileNameFormatting}.csv", "w", encoding="utf-8", newline="")
# csvWriter = csv.writer(fd)
# for li in datas_li:
#     csvWriter.writerow(li)
# fd.close()
# print("[INFO]   ", todayFileNameFormatting, ".csv generated")
#
#
# # log 출력
# log_fd = open("StormCrawler.txt", "a", newline="")
# log_fd.write(f"[Start Time] {startTime}\n")
# log_fd.write(f"[End Time] {endTime}\n")
# log_fd.write(f"[Running Time] : { endTime - startTime} (ms)\n")
# log_fd.write(f"[File Length] {countingURL} url, {len(datas_li)} rows \n\n")
# log_fd.close()
#
# print("[LOGGED] time log.txt generated")
#
#
# # 기존 csv에 추가
#
# fd2 = open("crawled flights.csv", "r", encoding="UTF-8")  # 마지막인덱스찾기
# csvReader = csv.reader(fd2)
# lastIdx = 1
# for i in csvReader:
#     lastIdx = i[0]
# lastIdx = int(lastIdx)
# print("lastidx : ", lastIdx)
# fd2.close()
# for i in range(len(datas_li)):
#     datas_li[i][0] = i + lastIdx + 1
#
# fd3 = open("crawled flights.csv", "a", encoding="utf-8", newline="")
# csvWriter = csv.writer(fd3)
# for li in datas_li:
#     csvWriter.writerow(li)
# fd3.close()
# print("[UPDATE] flights.csv updated")