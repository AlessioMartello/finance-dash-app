from dash import Dash, html
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(

            className="relative-div",

    children=[
                html.Div(id="containerA", children=
                            dbc.Button('a btton')
                        ),
                html.Div(className="spinnerContainer",children=

                html.Div(id="spinner-div", children=[
                    dbc.Spinner(spinner_style={"width": "4rem", "height": "4rem"}, id="myspinner", fullscreen=True,
                                color="#7026b9", delay_hide=9000)
                ]
                         )
                )

            ]
                    )

if __name__ == "__main__":
    app.run_server(debug=False)
