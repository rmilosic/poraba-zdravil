import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html


import app.components as components


trends_layout = [
    dbc.Row(
        className="justify-content-between",
        children=[
            dbc.Col(
                md=8,
                className="shadow-sm bg-white",
                children=[
                    dcc.Graph(
                        id="trend-graph-absolute"
                    )
                ]
            ),

            dbc.Col(
                md=3,
                children=components.trend_filters.layout
            )
        ]
    ),
    dbc.Row(
        className="my-4",
        children=[
            dbc.Col(
                className="p-0",
                children=[
                    html.Div(
                        id="trend-table"
                    )
                ]
            )
        ]
    )
]


year_layout = [

]

