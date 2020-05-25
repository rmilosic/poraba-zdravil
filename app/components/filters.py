import dash_core_components as dcc
import dash_html_components as html

import dash_bootstrap_components as dbc

from app.components import filter_layout


year_slider_component = dcc.Slider(
    id='year-slider',
    min=2010,
    max=2019,
    step=1,
    value=2019,
    tooltip={
        "always_visible": True
    },
    marks={
        2010: "2010",
        2019: "2019"
    },
)

year_slider = filter_layout.create_filter_layout("Izberi leto", year_slider_component)

aggregate_value_dropdown = html.Div(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H4(
                            "Primerjaj glede na"
                        )
                    ]
                )
            ]
        ),

        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dcc.Dropdown(
                            id="aggregate-value-radio",
                            options=[
                                {'label': 'Celotna vrednost receptov', 'value': 'Celotna vrednost receptov'},
                                {'label': 'Število DDD', 'value': 'Stevilo DDD'},
                                {'label': 'Število DID', 'value': 'Stevilo DID'},
                                {'label': 'Vrednost OZZ', 'value': 'Vrednost OZZ'},
                                {'label': 'Število receptov', 'value': 'Število receptov'},
                                {'label': 'Število škatel', 'value': 'Število škatel'}
                            ],
                            value="Celotna vrednost receptov"
                        )]
                )
            ]
        )
    ]
)

atc_level_dropdown = html.Div(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    className="my-3",
                    children=[
                        html.H4(
                            "Izberi nivo ATC"
                        )
                    ]
                )
            ]
        ),

        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dcc.Dropdown(
                            id="atc-level-dropdown",
                            options=[dict(label=f"ATC {i}", value=f"ATC{i}") for i in range(1, 6)],
                            value="ATC1"
                        )]
                )
            ]
        )
    ]
)
