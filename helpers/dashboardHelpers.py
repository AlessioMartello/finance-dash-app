import base64
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dash_table
from pathlib import Path
from dash import dcc
from dash import html
from googleDrive.helpers import chooseFileId, getFile

root = Path(__file__).parent.parent

def createHistoricalBalances(transDf):
    # Create figure with secondary y-axis
    HistoricBalancesFig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    HistoricBalancesFig.add_trace(
        go.Scatter(x=transDf["date"], y=transDf["amount"], name="Transaction amount",
                   customdata=transDf["name"].tolist()),
        secondary_y=False,
    )

    HistoricBalancesFig.update_traces(
        hovertemplate="%{y}<br>%{customdata}<br> ",
        mode="lines"
    )

    HistoricBalancesFig.add_trace(
        go.Scatter(x=transDf["date"], y=transDf["balance"], name="Balance"),
        secondary_y=True,
    )

    # Add figure title
    HistoricBalancesFig.update_layout(
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        height=800,
        title_font_color="white",
        title_font_size=20,
        legend_font_color="grey",
        legend_font_size=20,
        plot_bgcolor='rgb(34,34,34)',

    )

    # Set x-axis title
    HistoricBalancesFig.update_xaxes(title_text="Date", color="white", title_font_size=20, gridcolor="white")

    # Set y-axes titles
    HistoricBalancesFig.update_yaxes(title_text="Transaction", secondary_y=False, color="white", title_font_size=20,
                                     gridcolor="white")
    HistoricBalancesFig.update_yaxes(title_text="Balance", secondary_y=True, color="white", title_font_size=20,
                                     gridcolor="white")

    return HistoricBalancesFig


def returnTransDatatable(df_unformatted):
    """Returns the datatable to be used in the filter function"""
    df = df_unformatted.copy()
    for col in df:
        if col == "date" or col == "datetime":
            df[col] = pd.DatetimeIndex(df[col]).strftime("%d-%m-%Y")

    return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True,)


dataTableFormatting = {"style_header": {
    'backgroundColor': 'rgb(30, 30, 30)',
    'color': 'white',
    'textAlign': 'center'
},
    "style_data": {
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white',
        'height': 'auto',
    },
    "style_cell": {"textAlign": "center"},
    "style_cell_conditional": [
        {
            'textAlign': 'center'
        }
    ]
}


def createMonthlySpendingFigure(monthlySpending):
    """Returns the table with spending for this month only"""
    monthlySpendingFig = dash_table.DataTable(monthlySpending.to_dict('records'),
                                              [{"name": i, "id": i} for i in monthlySpending.columns],
                                              style_header=dataTableFormatting["style_header"],
                                              style_cell=dataTableFormatting["style_cell"],
                                              style_data=dataTableFormatting["style_data"],
                                              style_cell_conditional=dataTableFormatting["style_cell_conditional"],
                                              fill_width=True,
                                              style_table={'overflowY': 'auto'}
                                              )

    return monthlySpendingFig


def createBalanceFigure(releventBalances):
    """Returns the formatted df extracted from the balances endpoint"""
    releventBalances.round()
    Balancefig = dash_table.DataTable(releventBalances.to_dict('records'),
                                      [{"name": i, "id": i} for i in releventBalances.columns],
                                      style_header=dataTableFormatting["style_header"],
                                      style_cell=dataTableFormatting["style_cell"],
                                      style_data=dataTableFormatting["style_data"],
                                      style_cell_conditional=dataTableFormatting["style_cell_conditional"],
                                      fill_width=True,
                                      )

    return Balancefig


def createPieChart(catgoryCounts):
    """ Makes the Category counts pie chart"""
    PieChartfig = px.pie(catgoryCounts, values='Counts', names='categories')
    PieChartfig.update_layout(paper_bgcolor="rgba(0,0,0,0)", title_font_color="white",
                              legend_font_color="grey", legend_font_size=20)
    return PieChartfig


def addTitle(text):
    """ Formats the text to use as a figure title"""
    mkdw = f"""{text}"""
    return dcc.Markdown(children=mkdw)

def cleanCategories(df):
    """Clean the raw data to more readable description"""
    df["name"] = df["name"].str.replace(
        " ON (.*)|,(.*)|CARD PAYMENT TO |FASTER PAYMENTS RECEIPT REF.|DIRECT DEBIT PAYMENT TO |REGULAR TRANSFER ", "",
        regex=True).str.capitalize()
    return df

def createTransactionsThisMonth(df):
    """Expects transactions only from this month"""
    inThisMonth = df[df["amount"] > 0]
    outThisMonth = df[df["amount"] < 0]

    # Create figure with secondary y-axis
    transactionsThisMonthFig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    transactionsThisMonthFig.add_trace(
        go.Scatter(x=inThisMonth["datetime"], y=inThisMonth["amount"], name="In",
                   customdata=inThisMonth["name"].tolist()),
        secondary_y=False,
    )



    transactionsThisMonthFig.add_trace(
        go.Scatter(x=outThisMonth["datetime"], y=outThisMonth["amount"], name="Out",
                   customdata=outThisMonth["name"].tolist()),
        secondary_y=True
    )
    transactionsThisMonthFig.update_traces(
        hovertemplate="%{y}<br>%{customdata}<br> ",
        mode="lines"
    )
    # Add figure title
    transactionsThisMonthFig.update_layout(
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        height=800,
        title_font_color="white",
        title_font_size=20,
        legend_font_color="grey",
        legend_font_size=20,
        plot_bgcolor='rgb(34,34,34)',

    )

    # Set x-axis title
    transactionsThisMonthFig.update_xaxes(title_text="Date", color="white", title_font_size=20, gridcolor="white")

    # Set y-axes titles
    transactionsThisMonthFig.update_yaxes(title_text="In", secondary_y=False, color="white", title_font_size=20,
                                     gridcolor="white")
    transactionsThisMonthFig.update_yaxes(title_text="Out", secondary_y=True, color="white", title_font_size=20,
                                     gridcolor="white")

    return transactionsThisMonthFig

def makeHeader(text):
    """Produces the Navbar-type Row element used in each tab"""
    imgFile = getFile(chooseFileId("am_logo_white.png")).read() # read logo in as bytes
    encoded_image = base64.b64encode(imgFile)
    return dbc.Row([
        dbc.Col(html.A(href="https://www.artlessi.co.uk", target="_blank", rel="noopener noreferrer", children=
            html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={"height": "20vh"})
        )
            ),
        dbc.Col(
            html.H1('Alessio\'s personal finance app', className="text-center"),style={"color":"rgb(112,38,185)"}),
        dbc.Col(dcc.Markdown(children=text))
    ], justify="center", align="center", )


if __name__ == '__main__':
    pass
