# coding = utf-8

import pymysql
import pandas as pd
import numpy as np
import seaborn as sns


# 강남역에서 출퇴근 하기 좋은 아파트 확인하기
apt_tot=pd.read_pickle("apt_tot.pkl")

# 경기도 시도명 확인
apt_tot=apt_tot.reset_index(drop=False)
temp=apt_tot.loc[apt_tot["시도명"].isin(["경기도"])]
temp["시군구명"].value_counts()

# 구리시, 하남시, 성남시
apt_tot=apt_tot.reset_index(drop=False)
apt_kkd=apt_tot.loc[apt_tot["시군구명"].str[0:3].isin(["구리시","하남시","성남시"])]
apt_kkd["시도명"].value_counts()

import tat
tat.distplot(data=apt_kkd, x="전세가_비율", hue="시군구명")

# 70%이상 추출하기
apt_kkd_70 = apt_kkd[apt_kkd["전세가_비율"]>0.7]
len(apt_kkd_70)

apt_kkd_70["주소"]=apt_kkd_70["시도명"]+" "+apt_kkd_70["시군구명"] + " " +  apt_kkd_70["동"] +" "+ apt_kkd_70["지번"] +" "+ apt_kkd_70["아파트명"]
apt_kkd_70=apt_kkd_70.reset_index(drop=True)
juso=apt_kkd_70["주소"][0]

from urllib.request import urlopen
from urllib.parse import quote
import time
import json
import random

# https://developers.google.com/maps/documentation/directions/intro#TravelModes

api_key="발급받은 API키를 입력합니다."
apt_kkd_70["시간"]=""

for idx, juso in enumerate(apt_kkd_70["주소"]):
    try:
        url="https://maps.googleapis.com/maps/api/directions/json?origin="+quote(juso)+"&destination="+quote("강남역")+"&mode=transit&key="+api_key
        result=urlopen(url).read()
        json_result = json.loads(result)
        dur_time = json_result["routes"][-1]["legs"][-1]["duration"]["text"]
        apt_kkd_70.loc[apt_kkd_70["주소"]==juso,"시간"] = dur_time
        print("{}: {}, {}".format(idx,juso,dur_time))
    except Exception as e:
        print(e)

    time.sleep(random.randint(1,3))

apt_kkd_70.head()

def change_to_m(x):
    if x=="":
        return None

    if x.find("hours")>-1:
        h=x.split(" hours")[0]
        h=int(h)*60
        x=x.split(" hours")[1]
    elif x.find("hour")>-1:
        h=x.split(" hour")[0]
        h=int(h)*60
        x=x.split(" hour")[1]
    else:
        h=0

    m=x.split(" min")[0]
    m=int(m)

    return h+m

apt_kkd_70["대중"]=apt_kkd_70["시간"].apply(change_to_m)
len(apt_kkd_70)

apt_kkd_70_1 = apt_kkd_70[apt_kkd_70["대중"].isnull()==False]
len(apt_kkd_70_1)

tat.distplot(data=apt_kkd_70_1, x="대중", hue="시군구명")

sns.scatterplot(data=apt_kkd_70_1, x="전세가_비율", y="대중", hue="평수구분")

temp = apt_kkd_70_1[(apt_kkd_70_1["대중"]<50) & (apt_kkd_70_1["전세가_비율"]>0.85)]
print(temp)