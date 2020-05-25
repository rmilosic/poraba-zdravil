from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_table


def print_name(name, word_count_threshold=7, break_point_ratio=0.6):
    """Splits name of item in legend into 2 lines
    if word count exceeds threshold"""
    words = name.split(" ")
    word_count = len(words)

    if word_count > word_count_threshold:

        position = round(word_count*break_point_ratio)
        words.insert(position, "<br>")

        return ' '.join(words)
    else:
        return name


def register_callbacks(app, df):
    """
    Register app callbacks
    """
    @app.callback(
        Output('trend-graph-absolute', 'figure'),
        [
            Input('aggregate-value-radio', 'value'),
            Input('atc-level-dropdown', 'value')
        ]
    )
    def update_main_graph(aggregate_value_name: str, atc_level: int):

        df2 = df.loc[df[aggregate_value_name] > 0]

        df_pivot = df2.pivot_table(
            index=["leto", atc_level],
            values=aggregate_value_name,
            aggfunc=sum
        ).unstack(1)

        categoryarray = df_pivot.loc[df_pivot.index.max()].sort_values(ascending=False).index

        fig = go.Figure()

        for col in categoryarray:

            fig.add_trace(
                go.Bar(
                    x=df_pivot.index.to_list(), y=df_pivot[col].to_list(), name=print_name(col[1])
                )
            )

        fig.update_layout(
            title="Pregled porabe po ATC skupinah",
            barmode='stack',
            xaxis={'categoryorder': 'sum descending', "tickmode": "linear"},
            legend_orientation="v",
            legend={"font": {"size": 9}})

        return fig

    @app.callback(
        Output('trend-table', 'children'),
        [
            Input('aggregate-value-radio', 'value'),
            Input('atc-level-dropdown', 'value')
        ]
    )
    def update_trends_table(aggregate_value_name: str, atc_level: int):

        df2 = df.loc[df[aggregate_value_name] > 0]

        df_pivot = df2.pivot_table(
            index=[atc_level],
            columns="leto",
            values=aggregate_value_name, aggfunc=sum
        )

        df_pivot = df_pivot.reset_index()

        out_data = df_pivot.sort_values(by=2019, ascending=False).round().to_dict('records')
        out_columns = [{"name": f"{i}", "id": f"{i}"} for i in df_pivot.columns]

        return [dash_table.DataTable(
            columns=out_columns,
            data=out_data,
            style_data={
                'whiteSpace': 'normal',
            },
            style_cell={'overflow': 'hidden', 'textAlign': 'left', 'maxWidth': 50, 'textOverflow': 'ellipsis'}
        )]

    # YEAR view
    @app.callback(
        Output('year-graph-absolute', 'figure'),
        [
            Input('year-slider', 'value'),
            Input('aggregate-value-radio', 'value'),
            Input('atc-level-dropdown', 'value')
        ]
    )
    def update_year_graph(year_slider_value: int, aggregate_value_name: str, atc_level: int):

        df2 = df.loc[(df[aggregate_value_name] > 0) & (df.leto == year_slider_value)]

        df_pivot = df2.pivot_table(
            index=[atc_level],
            values=aggregate_value_name,
            aggfunc=sum
        )

        fig = go.Figure([
            go.Bar(
                y=[i[:30]+"..." for i in df_pivot.index.to_list()], x=df_pivot[aggregate_value_name],
                orientation="h"
            )
        ])

        fig.update_layout(
            title="Pregled porabe po ATC skupinah",
            yaxis={
                "automargin": True,
                "categoryorder": "total ascending",
                "title": {
                    "standoff": 1
                },
                "tickfont": {
                    "size": 10
                }
            },
            margin={"l": 200}
        )

        return fig

    @app.callback(
        Output('year-table', 'children'),
        [
            Input('year-slider', 'value'),
            Input('aggregate-value-radio', 'value'),
            Input('atc-level-dropdown', 'value')
         ]
    )
    def update_trends_table(year_slider_value, aggregate_value_name: str, atc_level: int):
        df2 = df.loc[(df[aggregate_value_name] > 0) & (df.leto == year_slider_value)]

        df_pivot = df2.pivot_table(
            index=[atc_level],
            values=aggregate_value_name,
            aggfunc=sum
        )

        df_pivot = df_pivot.reset_index()

        out_data = df_pivot.sort_values(by=aggregate_value_name, ascending=False).round().to_dict('records')
        out_columns = [{"name": f"{i}", "id": f"{i}"} for i in df_pivot.columns]

        return [
            dash_table.DataTable(
                columns=out_columns,
                data=out_data,
                style_data={
                    'whiteSpace': 'normal',
                    #             'height': 'auto'
                },
                style_cell={'overflow': 'hidden', 'textAlign': 'left', 'maxWidth': 50, 'textOverflow': 'ellipsis'}
            )
        ]
