import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import dash_bootstrap_components as dbc


from app.callbacks import register_callbacks
from app.components import navigation
from app.layouts import layouts

# load data
df = pd.read_csv("data/processed/final_dataset_10_19.csv", encoding="utf-8")


years = df.leto.unique()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA], suppress_callback_exceptions=True)


app.layout = html.Div(
    style={"backgroundColor": "#fafafa"},
    children=[
        dcc.Location(id='url', refresh=False),
        navigation.layout,
        html.Div(id='page-content')
    ]
)

index_page = html.Div([
    dcc.Link('Trendi', href='/trendi'),
    html.Br(),
    dcc.Link('Leto', href='/leto'),
])


register_callbacks(app, df)


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/trendi':
        return dbc.Container(
            children=layouts.trends_layout
        )
    elif pathname == '/leto':
        return dbc.Container(
            children=layouts.trends_layout
        )
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True)