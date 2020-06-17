# coding = utf-8

import pymysql
import pandas as pd
import numpy as np
import seaborn as sns

db_conf = {
    "host": "127.0.0.1",
    "user": "test",
    "password": "test11",
    "database": "finance",
}

con = pymysql.connect(**db_conf)
apt_sale = pd.read_sql("SELECT * FROM APT_SALE WHERE YM>=201911 AND YM<=202001", con)
apt_lent = pd.read_sql("SELECT * FROM APT_LENT WHERE YM>=201911 AND YM<=202001", con)
con.close()

apt_sale.columns = ["매매가격", "건축년도", "년", "월", "일", "동", "아파트명", "크기", "지번", "코드", "층", "년월", "id", "시간"]
apt_lent.columns=["건축년도","년","동","보증금가격","아파트명","월","월세","거래일","크기","지번","코드","층","년월","id","시간"]

# 시도명을 붙입니다.
ji_code = pd.read_excel("./data/KIKcd_B.20181210.xlsx")
ji_code["코드"] = ji_code["법정동코드"].astype(str).str[0:5]
ji_code_nodup = ji_code[["코드", "시도명", "시군구명"]].drop_duplicates()

apt_sale = pd.merge(apt_sale, ji_code_nodup, on="코드", how="left")
apt_lent = pd.merge(apt_lent, ji_code_nodup, on="코드", how="left")

# 아파트 평수를 나눕니다.
label = ["10평미만", "10평대","20평대", "30평대", "40평대", "50평대", "60평대", "60평대 이상"]
apt_sale["평수"] = apt_sale["크기"]/3.3
apt_sale["평수구분"] = pd.cut(apt_sale["평수"], [0,10, 20, 30,40,50, 60,70,np.Inf], labels=label)

apt_lent["평수"] = apt_lent["크기"]/3.3
apt_lent["평수구분"] = pd.cut(apt_lent["평수"], [0,10, 20, 30,40,50, 60,70,np.Inf], labels=label)

# 전세 데이터만 추출합니다.
apt_lent_j = apt_lent.loc[apt_lent["월세"]==0]

# 평균거래가격을 계사합니다.
apt_sale_gr = apt_sale.groupby(["시도명", "시군구명", "동", "지번" ,"아파트명", "평수구분"]).agg({"매매가격":"mean","아파트명":"size"})
apt_sale_gr.columns = ["매매가_평균", "매매거래건수"]

apt_lent_j_gr = apt_lent_j.groupby(["시도명", "시군구명", "동","지번" ,"아파트명", "평수구분"]).agg({"보증금가격":"mean","아파트명":"size"})
apt_lent_j_gr.columns = ["전세가_평균", "전세거래건수"]

# 거래건수 비중
sns.countplot(apt_sale_gr["매매거래건수"], label="small")
sns.countplot(apt_lent_j_gr["전세거래건수"], label="small")

# 매매, 전세 데이터 결합
apt_tot = pd.merge(apt_lent_j_gr, apt_sale_gr, how="inner", left_index=True, right_index=True)

apt_tot["전세가_비율"]=apt_tot["전세가_평균"]/apt_tot["매매가_평균"]
pd.set_option('display.max_columns', 100)
apt_tot.sort_values("전세가_비율", ascending=False)
apt_tot.head()

# 전세가비율 그래프 그리기
import numpy as np
g = sns.distplot(apt_tot["전세가_비율"])
g.set_xticks(np.arange(0,2.5,0.1))
apt_tot.to_pickle("apt_tot.pkl")
