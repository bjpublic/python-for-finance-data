# coding = utf-8
import dash
import dash_core_components as dcc

app = dash.Dash(__name__)

app.layout = dcc.Markdown(
    """
    ### 안녕하세요.
    ** 반갑습니다. **
    - 오늘도 또 만났네요
    """
)

if __name__ == '__main__':
    app.run_server(debug=True, port=9999)
