import pymysql
import pandas as pd
import seaborn as sns

# 통화량 데이터 가져오기
db_conf = {
    "host": "127.0.0.1",
    "user": "test",
    "password": "test11",
    "database": "finance",
}

con = pymysql.connect(**db_conf)
df = pd.read_sql("SELECT * FROM kor_bank WHERE stat_code='001Y453'", con)
con.close()

# 데이터 타입 변경
df["data_value"]=df["data_value"].astype(float)

df["time"]=df["time"]+"01"
df["time"]=df["time"].astype('datetime64')
df["time"] = df["time"] + pd.offsets.MonthEnd()

sns.lineplot(data=df, x="time", y="data_value", hue="item_code1")

df["change_ratio"]=df.groupby("item_code1")["data_value"].pct_change(12)*100
# a=df[["change_ratio","data_value","item_code1","time"]].head(100)
sns.lineplot(data=df, x="time", y="change_ratio", hue="item_code1",
             style="item_code1")

# 주가지수 수집하기
import FinanceDataReader as fdr

# KOSPI지수 수집하기
df_kospi = fdr.DataReader('KS11', '2015')
df_kospi.head()

kospi_mean=df_kospi.resample('M', how="mean")
kospi_mean["change_ratio"]=kospi_mean["Close"].pct_change(12)*100
kospi_mean["item_code1"]="kospi"
kospi_mean=kospi_mean.reset_index(drop=False)
kospi_mean=kospi_mean.rename(columns={"Date":"time","Close":"data_value"})

df=pd.concat([df[["time","item_code1","data_value","change_ratio"]],
              kospi_mean[["time","item_code1","data_value","change_ratio"]]],0)

df_graph=df[df["item_code1"].isin(["BBHA00","kospi"])]
sns.lineplot(data=df_graph, x="time", y="change_ratio", hue="item_code1",
             style="item_code1",alpha=0.8)

# 아파트 매매 데이터 불러오기
con = pymysql.connect(**db_conf)
df_apt = pd.read_sql("SELECT ym,avg(price) FROM apt_sale WHERE ym>='201501' and ym<='201912' GROUP BY ym", con)
con.close()

# 전년동월대비 증감율 구하기
df_apt["change_ratio"]=df_apt["avg(price)"].pct_change()*100

# 시간과 매매가격 데이터 타입 맞추
df_apt.columns=["time","data_value","change_ratio"]
df_apt["time"]=df_apt["time"]*100+1
df_apt["time"]=df_apt["time"].astype(str).astype('datetime64')
df_apt["time"] = df_apt["time"] + pd.offsets.MonthEnd()
df_apt["item_code1"]="APT"

# 그래프 그리기
df_graph=pd.concat([df_graph,df_apt],0)
df_graph.index=df_graph["time"]
df_graph=df_graph["2016":]
sns.set_style("whitegrid")
sns.lineplot(data=df_graph, x="time", y="change_ratio", hue="item_code1",
             style="item_code1", markers=True, alpha=0.8)

# df_graph1["time"]=df_graph1["time"].astype(int)
# sns.lmplot(data=df_graph1, x="time", y="change_ratio", hue="item_code1", order=3)

from sklearn.preprocessing import MinMaxScaler
import numpy as np

#최소-최대 정규화
scaler=MinMaxScaler()
df_graph1=pd.DataFrame()
for d in df_graph.groupby("item_code1"):
    d[1]["cr_minmax"]=scaler.fit_transform(d[1][["change_ratio"]])
    df_graph1=pd.concat([df_graph1,d[1]],0)

sns.lineplot(data=df_graph1, x="time", y="cr_minmax", hue="item_code1",
             style="item_code1", markers=True, alpha=0.8)

df_graph_gr=df_graph1.groupby("item_code1")["cr_minmax"].rolling(6).mean()
df_graph_gr=df_graph_gr.reset_index(drop=False)
sns.lineplot(data=df_graph_gr, x="time", y="cr_minmax", hue="item_code1",
             style="item_code1")