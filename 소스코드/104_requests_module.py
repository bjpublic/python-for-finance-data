import requests

input_data = {"pGB":1, "gicode":"A005930"}
result = requests.get("http://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp", data=input_data)
print(result.text)

# beautifulsoupdㅡ로 파싱
from bs4 import BeautifulSoup
soup = BeautifulSoup(result.text, 'html.parser')
soup_table = soup.find("table", attrs={"class":"us_table_ty1 h_fix zigbg_no"})

# 판다스 데이터프레임으로 변환
from html_table_parser import parser_functions as parser
import pandas as pd

table = parser.make2d(soup_table)
df = pd.DataFrame(table[1:], columns=table[0])
df.head()