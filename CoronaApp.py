import pathlib

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go
import datetime
import pandas as pd
import requests
import plotly.express as px
from plotly.subplots import make_subplots
import requests


from iexfinance.stocks import get_historical_data


start = datetime.datetime.today() - relativedelta(years=5)
end = datetime.datetime.today()
# API Requests for news div
news_requests = requests.get(
    "http://newsapi.org/v2/top-headlines?country=ma&apiKey=9954e86486a5468eba3adc8943a53389"
)

# API Call to update news
def update_news():
    json_data = news_requests.json()["articles"]
    df = pd.DataFrame(json_data)
    df = pd.DataFrame(df[["title", "url"]])
    max_rows = 10
    return html.Div(
        children=[
            html.P(className="p-news", children="Headlines"),
            html.P(
                className="p-news float-right",
                children="Last update : "
                + datetime.datetime.now().strftime("%H:%M:%S"),
            ),
            html.Table(
                className="table-news",
                children=[
                    html.Tr(
                        children=[
                            html.Td(
                                children=[
                                    html.A(
                                        className="td-link",
                                        children=df.iloc[i]["title"],
                                        href=df.iloc[i]["url"],
                                        target="_blank",
                                    )
                                ]
                            )
                        ]
                    )
                    for i in range(min(len(df), max_rows))
                ],
            ),
        ]
    )


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()


app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H2("Corona Virus Application"),
        html.Img(src="/assets/covid.png")
    ], className="banner"),

    html.Div([
        html.H3('HAMDOUCHI Abderahmane   "MASTER SDAD"')

    ]),
    html.Div([
        dcc.Dropdown(
            id='demo-dropdown',
            options=[
                {'label': 'Bares par statuts', 'value': 0},
                {'label': 'statuts par date', 'value': 1},
                {'label': 'Statuts par région ', 'value': 2}
            ],
            value=0
            ,className="four columns"
        )
    ],className="row"),


    html.Div([
        html.Div([
            dcc.Graph(
                id="graph_close",
            )
        ], className="eight columns"),

        html.Div([
            html.H3("Journal du Maroc"),
            update_news()
        ], className="four columns"),

    ],className="row")
])

app.css.append_css({
    "external_url":"https://codepen.io/chriddyp/pen/bWLwgP.css"
})



@app.callback(Output('graph_close', 'figure'),
              [Input("demo-dropdown", "value")],
              )


def update_fig(value):
    df_new = pd.read_csv(DATA_PATH.joinpath("corona_maroc.csv"))


    fig = make_subplots(rows=1, cols=2)

    fig.add_trace(
        go.Scatter(y=df_new['province'].value_counts(), x=df_new['province'].value_counts().index, mode="lines"), row=1,
        col=1)

    fig.add_trace(go.Bar(y=df_new['province'].value_counts(), x=df_new['province'].value_counts().index), row=1, col=2)
    trace_bar = fig

    trace_line =go.Figure( data=[go.Bar(y=df_new['state'].value_counts() , x=df_new['state'].value_counts().index)], layout_title_text="La distribution de statut des gens infectés par Corona")

    trace_candle = px.scatter(df_new, x="province", y="confirmed_date", color="state", title="A Plotly Express Figure")
    data = [trace_line, trace_candle, trace_bar]





    return  data[value]

if __name__=="__main__":
    app.run_server(debug=True, port=5001)