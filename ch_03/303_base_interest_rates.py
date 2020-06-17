from urllib.request import urlopen
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parser
import pymysql
import pandas as pd
import time


# 외국금리
# https://www.global-rates.com/interest-rates/central-banks/central-bank-japan/boj-interest-rate.aspx

def get_for_rate(nation,to="2019-12-31"):

    nation_list={"KOR":"/central-bank-south-korea/bank-of-korea-interest-rate.aspx",
                 "JPN":"/central-bank-japan/boj-interest-rate.aspx",
                 "USA":"/central-bank-america/fed-interest-rate.aspx",
                 "CHI":"/central-bank-china/pbc-interest-rate.aspx",
                 "EUR":"/european-central-bank/ecb-interest-rate.aspx"
                 }

    url=nation_list.get(nation, "-1")

    if url=="-1":
        print("국가명을 확인해주세요.")
        return -1

    url="https://www.global-rates.com/interest-rates/central-banks{}".format(url)
    result=urlopen(url).read()
    soup=BeautifulSoup(result,"html.parser")
    table_tags=soup.find_all("table")

    # for idx,t in enumerate(table_tags):
    #     try:
    #         print("{}: ".format(idx),end="")
    #         print(t.find_all("h3")[0].text)
    #     except:
    #         pass

    table = parser.make2d(table_tags[18])
    df = pd.DataFrame(table[2:], columns=table[1])
    df.head()

    df["dt"]=df["change date"].astype("datetime64")
    df_range=pd.DataFrame({"dt":pd.date_range(df["dt"].min(),to)})

    df_1=pd.merge(df_range,df,how="left")
    df_1["percentage"]=df_1["percentage"].fillna(method="ffill")
    df_1["percentage"]=df_1["percentage"].str.replace("\xa0%","").astype(float)

    df_1["nation"]=nation
    df_1=df_1.drop("change date",1)
    df_1=df_1.rename(columns={"percentage":"base_rate"})

    time.sleep(3)

    return df_1


# 국가별 기준 금리 정보를 수집합니다.
df_kor=get_for_rate("KOR")
df_jpn=get_for_rate("JPN")
df_usa=get_for_rate("USA")
df_chi=get_for_rate("CHI")
df_eur=get_for_rate("EUR")
df=pd.concat([df_kor,df_jpn,df_usa,df_chi,df_eur],0)

# 모든 국가에 포함된 시작일자를 구합니다.
df_min_dt=df.groupby('nation')["dt"].min()
df_min_dt=max(df_min_dt)
df_graph=df.loc[df["dt"]>=df_min_dt]

import seaborn as sns
sns.lineplot(data=df_graph,x="dt",y="base_rate",hue="nation", alpha=0.7)


# 금리 관련 뉴스 정보를 수집합니다.
API_KEY="96f5b5ce63766554fbcb884684641572"
word="금리"

from urllib.parse import quote

url="https://gnews.io/api/v3/search?q={}&lang=ko&token={}".format(quote(word),API_KEY)
result=urlopen(url)
html=result.read()


import urllib.request
import json

client_id = "발급받은 Client ID를 넣습니다."
client_secret = "발급받은 Client Secret을 넣습니다."
encText = urllib.parse.quote("금리")
url = "https://openapi.naver.com/v1/search/news.json?query=" + encText # json 결과

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)

res=response.read()
result=json.loads(res)
