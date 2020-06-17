# coding = utf-8
import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px

import pymysql
import pandas as pd

def apt_deal_cnt():
    db_conf = {
        "host": "127.0.0.1",
        "user": "test",
        "password": "test11",
        "database": "finance",
    }

    con = pymysql.connect(**db_conf)
    apt_sale = pd.read_sql("SELECT * FROM APT_SALE WHERE YM>=201911 AND YM<=201912", con)
    con.close()

    apt_sale.columns = ["매매가격", "건축년도", "년", "월", "일", "동", "아파트명", "크기", "지번", "코드", "층", "년월", "id", "시간"]

    ji_code = pd.read_excel("./data/KIKcd_B.20181210.xlsx")
    ji_code["코드"] = ji_code["법정동코드"].astype(str).str[0:5]
    ji_code_nodup = ji_code[["코드", "시도명"]].drop_duplicates()
    apt_sale = pd.merge(apt_sale, ji_code_nodup, on="코드", how="left")

    g =px.histogram(apt_sale, x="시도명", y="시도명").update_xaxes(categoryorder="total descending")

    return g


app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='아파트 매매거래 건수'),
    html.Br(),
    dcc.Graph(figure=apt_deal_cnt())
])

if __name__ == '__main__':
    app.run_server(debug=True, port=9971)
