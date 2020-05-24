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
    @app.callback(
        Output('trend-graph-absolute', 'figure'),
        [Input('aggregate-value-radio', 'value'),
        Input('atc-level-dropdown', 'value'),
#         Input('atc-filter-type', 'value'),
#         Input('atc-filter-dropdown', 'value')
        ]
    )
    def update_main_graph(aggregate_value_name: str, atc_level: int #, atc_filter_type: str, atc_filter_values: list
    ):
        y_traces = []

        #         atc_filter_values =
        df2 = df.loc[ df[aggregate_value_name] > 0 ]

        df_pivot = df2.pivot_table(
            index=["leto", atc_level],
            values=aggregate_value_name,
            aggfunc=sum
        ).unstack(1)

#         print(df_pivot.head())
#         print(df_pivot.index.to_list())



        categoryarray = df_pivot.loc[df_pivot.index.max()].sort_values(ascending=False).index

#         print("cat array", categoryarray)

        fig = go.Figure()


        for col in categoryarray:
#             print(df_pivot[col].to_list())
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
        [Input('aggregate-value-radio', 'value'),
        Input('atc-level-dropdown', 'value'),
#         Input('atc-filter-type', 'value'),
#         Input('atc-filter-dropdown', 'value')
        ]
    )
    def update_trends_table(aggregate_value_name: str, atc_level: int #, atc_filter_type: str, atc_filter_values: list
    ):

        df2 = df.loc[ df[aggregate_value_name] > 0 ]

        df_pivot = df2.pivot_table(
            index=[atc_level],
            columns="leto",
            values=aggregate_value_name, aggfunc=sum)

#         df_pivot.index.set_names(["Leto"])
#         df_pivot.reset_index(inplace=True)


#         df_pivot.columns = df_pivot.columns.droplevel(0)
#         df_pivot.index = df_pivot.index.droplevel(0)

        df_pivot = df_pivot.reset_index()

#         print("pivot new", df_pivot)
#         print("pivot index", df_pivot.index)
#         print("pivot cols", df_pivot.columns)

        out_data = df_pivot.sort_values(by=2019, ascending=False).round().to_dict('records')
        out_columns = [{"name": f"{i}", "id": f"{i}"} for i in df_pivot.columns]

#         print("out data", out_data)
#         print("out cols", out_columns)

        return [dash_table.DataTable(
#             style_table={'overflowX': 'auto'},
            columns=out_columns,
            data=out_data,
            style_data={
            'whiteSpace': 'normal',
#             'height': 'auto'
            },
            style_cell={'overflow': 'hidden', 'textAlign': 'left', 'maxWidth': 50, 'textOverflow': 'ellipsis'}
        )]


