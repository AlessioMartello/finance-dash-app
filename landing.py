import re
import dash
import dash_auth
import dash_bootstrap_components as dbc
import os
from dotenv import load_dotenv
from dash import dcc
from helpers.KPIs import getTenLargestBuys
from helpers.dashboardHelpers import returnTransDatatable, makeHeader, addTitle, createHistoricalBalances, \
    createBalanceFigure, createMonthlySpendingFigure, createTransactionsThisMonth, createPieChart #,creditScoreLineChart,
from index import getDisplayData, getTransDf, todayDate, getTransThisMonth, getText, getBalances #,creditScoreFile,
from flask import request
from dash import html, Input, Output

VALID_USERNAME_PASSWORD_PAIRS = {
    'test': 'world'
}

load_dotenv()
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],
                )
app.config.suppress_callback_exceptions = True

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
    # {os.environ.get("valid_username"): os.environ.get("valid_password"),
    #  os.environ.get("valid_username2"): os.environ.get("valid_password2")}
)
server=app.server

def returnLandingPage():
    return html.Div([
        dbc.Row([
            dbc.Col(
                dbc.Button('Go to live data', href='/live', class_name="btn-lg")),
            dbc.Col(
                dbc.Button('Go to sample data', href='/sample', class_name="btn-lg"))
        ]
            , class_name="text-center align-items-center", style={"height": "80vh"}),
        dbc.Row(id="deny", children=dbc.Col("You are not authorised to access this, please select the sample data"),
                class_name="text-center align-items-center")])


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])


def returnPage(live=False):
    if live:
        transactionsFile, balancesDf = getDisplayData(live=True)
    else:
        transactionsFile, balancesDf = getDisplayData(live=False)
    transDf = getTransDf(transactionsFile, balancesDf)
    releventBalances = getBalances(balancesDf)
    transThisMonth = getTransThisMonth(transDf)
    textDict, kpiDict, minDate = getText(transDf, transThisMonth)

    return dbc.Container([dbc.Tabs(
        [
            dbc.Tab(label="Historic data", tab_id="tab1"),
            dbc.Tab(label="This month", tab_id="tab2"),
        ],
        id="tabs",
        active_tab="tab-one",
    ),

        html.Div(id="historic", children=
        [
            makeHeader(textDict["KPIText"])
            ,
            dbc.Row([addTitle(textDict["allTransactionsText"]), html.Div(id="my-div", style={"maxHeight": "50vh",
                                                                                             "overflow": "scroll",
                                                                                             "margin-bottom": "2rem"})]),
            dbc.Row([
                dbc.Col(
                    dcc.DatePickerRange(
                        id='my-date-picker-range',
                        min_date_allowed=minDate,
                        max_date_allowed=todayDate,
                        start_date=minDate,
                        end_date=todayDate,
                        display_format="DD MMM Y"
                    ), style={"width": "100%"}
                ),
                dbc.Col(dbc.Input(id="choose-kw", type="text", placeholder="Search for text from the name column")),
                dbc.Col(dbc.Input(id="choose-amount", type="number", placeholder="Enter a maximum amount"))],
                style={"text-align": "left", "padding-bottom": "3rem"}),
            dbc.Container(dbc.Row(html.Hr(
                style={'borderWidth': "5vh", "width": "100%", "color": "#FFFFFF", "height": ".8px", "opacity": 1})),
                          fluid=True, ),
            dbc.Row([addTitle(textDict["balanceHistoryText"]), dcc.Graph(
                id='Historic Balance Graph',
                figure=createHistoricalBalances(transDf)
            )], style={"text-align": "left"}),
            dbc.Row([
                dbc.Col([addTitle(textDict["monthlySpendingText"]),
                         createMonthlySpendingFigure(kpiDict["monthlySpending"])]),
                dbc.Col([dbc.Row([addTitle(textDict["balancesText"]), createBalanceFigure(releventBalances)]), dbc.Row(
                    [addTitle(textDict["pieChartText"]),
                     dcc.Graph(id='Pie chart', figure=createPieChart(kpiDict["catgoryCounts"]))],
                    style={"margin-top": "4rem"})]),
            ], style={"textAlign": "left"},
            ),
            # dbc.Row([dcc.Markdown(children=textDict["creditScoreText"]),
            #          dcc.Graph(id="line-chart-credit", figure=creditScoreLineChart(creditScoreFile))],
            #         style={"textAlign": "left"}),
        ], style={"padding": "2rem", 'textAlign': 'center', "display": "none"},
                 )
        ,
        html.Div(
            id="monthly", children=[
                makeHeader(textDict["thisMonthSpent"]),
                dbc.Row(
                    html.Div(dbc.Row(
                        [addTitle(textDict["thisMonthTransactionsTable"]), returnTransDatatable(transThisMonth)]
                    )
                        ,
                        style={"maxHeight": "50vh", "overflow": "scroll", "margin-bottom": "2rem", "margin-top": "2rem"}
                    )
                ),
                dbc.Row([
                    dbc.Col([
                        addTitle(textDict["thisMonthTransactionsGraph"]),
                        dcc.Graph(id="transactions-this-month", figure=createTransactionsThisMonth(transThisMonth))
                    ]),
                    dbc.Col([addTitle(textDict["topTenText"]), returnTransDatatable(getTenLargestBuys(transThisMonth))
                             ])
                ]
                )
            ]
        ),
    ]
        , fluid=True,
    )


@app.callback(
    [Output("historic", "style"),
     Output("monthly", "style")],
    [Input("tabs", "active_tab")],
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input and renders the tab content depending on what the value of
    'active_tab' is.
    """
    on = {'display': 'block'}
    off = {'display': 'none'}
    if active_tab is not None:
        if active_tab == "tab1":
            return [on, off]
        elif active_tab == "tab2":
            return [off, on]
    return [off, on]


@app.callback(
    Output(component_id='my-div', component_property='children'),
    # Output is from Function to App (and based on the input)
    Input('my-date-picker-range', 'start_date'),  # Input is from App to Function
    Input('my-date-picker-range', 'end_date'),
    Input('choose-kw', 'value'),
    Input('choose-amount', 'value'),
    Input('url', 'pathname')
)
def transactionDataFilter(start_date, end_date, kw, value, url):
    """Enable the datatable to be filtered per date, text in description and minimum transaction amount"""
    if url == '/live':
        transactionsFile, balancesDf = getDisplayData(live=True)
    else:
        transactionsFile, balancesDf = getDisplayData(live=False)
    transDf = getTransDf(transactionsFile, balancesDf)
    transDf_columnFiltered = transDf[
        ["name", "amount", "date", "payment_channel", "transaction_code", "merchant_name", "balance"]]
    if start_date is not None and end_date is not None and kw is not None and value is not None:
        transDf_dateFiltered = transDf_columnFiltered[
            (transDf_columnFiltered["date"] > start_date) & (transDf_columnFiltered["date"] < end_date) & (
                transDf_columnFiltered["name"].str.contains(kw, flags=re.IGNORECASE))
            & (transDf_columnFiltered["amount"] < value)]
        return returnTransDatatable(transDf_dateFiltered)
    elif start_date is not None and end_date is not None and value is None and kw is not None:
        transDf_dateFiltered = transDf_columnFiltered[
            (transDf_columnFiltered["date"] > start_date) & (transDf_columnFiltered["date"] < end_date) & (
                transDf_columnFiltered["name"].str.contains(kw, flags=re.IGNORECASE))]
        return returnTransDatatable(transDf_dateFiltered)

    elif start_date is not None and end_date is not None and kw is None and value is not None:
        transDf_dateFiltered = transDf_columnFiltered[
            (transDf_columnFiltered["date"] > start_date) & (transDf_columnFiltered["date"] < end_date) & (
                    transDf_columnFiltered["amount"] < value)]
        return returnTransDatatable(transDf_dateFiltered)
    else:
        transDf_dateFiltered = transDf_columnFiltered[
            (transDf_columnFiltered["date"] > start_date) & (transDf_columnFiltered["date"] < end_date)]
        return returnTransDatatable(transDf_dateFiltered)


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    username = request.authorization['username']
    # if pathname == '/live' and username == "test":
    #     return returnPage(live=True)
    if pathname == '/sample' and (username == "test" or username == os.environ.get("valid_username")):
        return returnPage(live=False)
    # elif pathname == "/live" and username != os.environ.get("valid_username"):
    #     return returnLandingPage()
    else:
        return returnLandingPage()


@app.callback(dash.dependencies.Output('deny', component_property='style'),
              [dash.dependencies.Input('url', 'pathname')])
def hide(pathname):
    username = request.authorization['username']
    if pathname == "/live" and username != os.environ.get("valid_username"):
        return {'display': 'block', "font-size": "xx-large"}
    else:
        return {'display': 'none', "font-size": "xx-large"}


if __name__ == '__main__':
    app.run_server(debug=True)
    # todo get the sample data to update