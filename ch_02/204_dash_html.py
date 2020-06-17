# coding = utf-8
import dash
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='안녕하세요.'),
    html.H3('반갑습니다.'),
    html.Div('또 만났네요.', style={'color':'blue', 'fontSize':16}),
    html.P('안녕히 가세요.', className='class1', id='p1'),
])

if __name__ == '__main__':
    app.run_server(debug=True)
