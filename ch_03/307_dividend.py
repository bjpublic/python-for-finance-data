# coding = utf-8
from selenium import webdriver
import time

# 보통중 데이터 수집
def get_div_data(browser,last_num,file_nm):
    search_btn = browser.find_element_by_id("image1")
    search_btn.click()

    # html소스를 가져와서, 원하는 위치를 찾습니다.
    html = browser.page_source

    from bs4 import BeautifulSoup
    from html_table_parser import parser_functions as parser
    import pandas as pd

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", attrs={"id":"grid1_body_table"})
    p = parser.make2d(table)
    df = pd.DataFrame(p[2:],columns=p[1])
    df.head()

    import time
    import random
    from tqdm import tqdm

    prev_no = 0
    prev_table = None

    for i in tqdm(range(0,200)):

        try:
            next_btn = browser.find_element_by_id("cntsPaging01_next_btn")
            next_btn.click()
        except:
            time.sleep(2)
            try:
                next_btn = browser.find_element_by_id("cntsPaging01_next_btn")
                next_btn.click()
            except:
                time.sleep(2)
                next_btn = browser.find_element_by_id("cntsPaging01_next_btn")
                next_btn.click()

        def get_html(browser, cnt):

            if cnt>=4:
                return -1, -1

            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')

            cur_no = soup.find("a", attrs={"class":"w2pageList_control_label w2pageList_label_selected"})
            cur_no = cur_no.text

            table = soup.find("table", attrs={"id": "grid1_body_table"})

            if cur_no!=prev_no and prev_table!=table:
                return cur_no, table
            else:
                time.sleep(1)
                get_html(browser, cnt+1)

        cur_no, table = get_html(browser, 1)

        if cur_no== -1:
            print("\n종료. 테이블 정보가 바뀌지 않았습니다.")
            break

        p=parser.make2d(table)
        temp=pd.DataFrame(p[2:],columns=p[1])
        df = pd.concat([df, temp],0)
        prev_no = cur_no
        prev_table = html

        if cur_no==str(last_num):
            print("\n최종 페이지 도달")
            break
        time.sleep(random.randrange(3,5))
        df.to_pickle(file_nm)


# 전체 데이터 수집하기
browser = webdriver.Chrome('/Applications/chromedriver')
browser.get("http://www.seibro.or.kr/websquare/control.jsp?w2xPath=/IPORTAL/user/company/BIP_CNTS01042V.xml&menuNo=286#")
time.sleep(5)
# 배당주 메뉴의 마지막 페이지번호, 저장할 파일명을 넣습니다.
get_div_data(browser,"96","stock_div.pkl")
