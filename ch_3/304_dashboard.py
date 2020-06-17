# coding = utf-8
import dash
import dash_core_components as dcc
import dash_html_components as html
import collect_base_interest_rates as gbr
import pandas as pd
import plotly.express as px

app=dash.Dash(__name__)

def get_interests_graph():
    df=pd.read_pickle("df_graph.pkl")
    fig=px.line(df, x="dt", y="base_rate", color="nation")

    return fig

def get_news():
    """
    :return: 네이버뉴스 검색 리스트
    """
    result=gbr.get_naver_news()

    items=result["items"]
    link_list=[]

    from datetime import datetime, timezone, timedelta
    now=datetime.now(timezone.utc) + timedelta(hours=9)
    now=datetime.strftime(now,"%Y-%m-%d %H:%M:%S")
    link_list.append(html.Div(children="뉴스 검색시간:{}".format(now),style={"text-align":"right"}))

    for i in items:
        exc_word=["&quot;","<b>","</b>"]
        title=i["title"]
        description=i["description"]

        for e in exc_word:
            title=title.replace(e,"")
            description=description.replace(e, "")

        #제목 링크 넣기
        link=html.A(title,href=i["originallink"],style={"font-size":"14pt"})
        link=html.Li(link)
        link_list.append(link)

        # 설명 추가
        description=html.Article(description)
        link_list.append(description)

        # 공백추가
        link_list.append(html.Br())

    return link_list

def serve_layout():

    return html.Div(children=[
        html.H3("주요각국 기준 금리 현황", style={'text-align': 'center'}),
        dcc.Graph(id="graph1", figure=get_interests_graph()),
        html.Br(),
        html.H3("금리 관련 주요 뉴스", style={'text-align': 'center'}),
        html.Div(children=get_news()),
    ])


app.layout=serve_layout

if __name__ == '__main__':
    app.run_server()
