# -*- coding: utf-8 -*-
from dash import Dash, dcc, html
import time

from dash.dependencies import Input, Output

app = Dash(__name__)

app.layout = html.Div(id="loader",children=[
    html.H1(children='Hello Dash')])

if __name__ == "__main__":
    app.run_server(debug=False)
