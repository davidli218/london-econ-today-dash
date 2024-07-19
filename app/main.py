import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output

from app.data_provider import datasets
from app.data_provider import datasets_label
from app.graph_helper import compose_housing_graph
from app.graph_helper import compose_lm_graph
from app.graph_helper import compose_travel_graph
from app.graph_helper import general_housing_graph
from app.graph_helper import general_lm_graph
from app.graph_helper import general_travel_graph

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
app.title = "London Economic Today Dashboard"

server = app.server
app.config.suppress_callback_exceptions = True


def description_card() -> html.Div:
    intro_md = "Economic data of London, including " \
               "**housing**, **travel**, and **labour market**. " \
               "Interact with the controls below to discover more insights."

    return html.Div(
        id="description-card",
        children=[
            html.H3("Welcome to the London Economic Today Dashboard"),
            html.Div(id="intro", children=dcc.Markdown(intro_md)),
        ],
    )


def control_card() -> html.Div:
    return html.Div(
        id="control-card",
        children=[
            html.P("Select Dataset"),
            dcc.Dropdown(
                id="ctl-dataset-sel",
                options={value: datasets_label[value] for value in datasets.keys()},
                value=list(datasets.keys())[0],
            ),
            html.Hr(),
            html.P("Select Display Range"),
            dbc.Row([
                dbc.Col(dcc.Dropdown(id="ctl-year-sel-start"), width=6),
                dbc.Col(dcc.Dropdown(id="ctl-year-sel-end"), width=6),
            ]),
            html.Br(),
            # Display the selected date range
            dcc.RangeSlider(
                0, 0, marks=None,
                id="disp-year-sel",
                tooltip={"placement": "bottom"},
                disabled=True,
            ),
            html.Hr(),
            html.P("Select View Type"),
            dmc.SegmentedControl(
                id="ctl-view-mode-sel",
                orientation="horizontal",
                fullWidth=True,
                data=[
                    {"label": "General", "value": "general"},
                    {"label": "Compose", "value": "compose"},
                ],
                value="compose",
            ),
            html.Br(),
            html.P("Select Data Value Graph Type"),
            dmc.SegmentedControl(
                id="ctl-value-graph-type",
                orientation="horizontal",
                fullWidth=True,
                data=[],
            ),
            html.Br(),
            html.P("Select Data Trends Graph Type"),
            dmc.SegmentedControl(
                id="ctl-trends-graph-type",
                orientation="horizontal",
                fullWidth=True,
                data=[],
            ),
        ],
    )


app.layout = dbc.Container(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("app_logo.png"))],
        ),
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), control_card()],
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                html.Div(
                    id="data_value_card",
                    children=[
                        html.B("Value Data"),
                        html.Hr(),
                        dcc.Graph(id="disp-graph-data-value"),
                    ],
                ),
                html.Div(
                    id="data_trends_card",
                    children=[
                        html.B("Annual Growth"),
                        html.Hr(),
                        dcc.Graph(id="disp-graph-data-trends"),
                    ],
                ),
            ],
        ),
    ],
)


# CB: Dataset selection >> Date range options
@app.callback(
    Output("ctl-year-sel-start", "options"),
    Output("ctl-year-sel-end", "options"),
    Output("ctl-year-sel-start", "value"),
    Output("ctl-year-sel-end", "value"),
    Output("disp-year-sel", "min"),
    Output("disp-year-sel", "max"),
    Input("ctl-dataset-sel", "value"),
    Input("ctl-year-sel-start", "value"),
    Input("ctl-year-sel-end", "value"),
)
def update_date_range_options(selected_dataset, start_date, end_date):
    dataset = datasets[selected_dataset]

    date_range = sorted(dataset['year'].unique())

    if start_date is None or start_date not in date_range:
        start_date = date_range[0]
    if end_date is None or end_date not in date_range:
        end_date = date_range[-1]

    date_range_options_start = [{'label': str(year), 'value': year} for year in date_range if year <= end_date]
    date_range_options_end = [{'label': str(year), 'value': year} for year in date_range if year >= start_date]

    return date_range_options_start, date_range_options_end, start_date, end_date, date_range[0], date_range[-1]


# CB: Date range selection >> Date range display
@app.callback(
    Output("disp-year-sel", "marks"),
    Output("disp-year-sel", "value"),
    Input("ctl-year-sel-start", "value"),
    Input("ctl-year-sel-end", "value"),
    Input("disp-year-sel", "min"),
    Input("disp-year-sel", "max"),
)
def update_date_range_display(start_date, end_date, min_date, max_date):
    args = [start_date, end_date, min_date, max_date]
    return {str(date): str(date) for date in args}, [start_date, end_date]


# CB: View selection >> Graph type options
@app.callback(
    Output("ctl-value-graph-type", "data"),
    Output("ctl-trends-graph-type", "data"),
    Output("ctl-value-graph-type", "value"),
    Output("ctl-trends-graph-type", "value"),
    Input("ctl-view-mode-sel", "value"),
)
def update_graph_types(view_type):
    graph_types = [
        {"label": "Line", "value": "line"},
        {"label": "Bar", "value": "bar"},
        {"label": "Heatmap", "value": "heatmap", "disabled": view_type == 'general'},
    ]

    return graph_types, graph_types, *['line', 'bar' if view_type == 'general' else 'heatmap']


# CB: Data selection >> Graphs
@app.callback(
    Output("disp-graph-data-value", "figure"),
    Output("disp-graph-data-trends", "figure"),
    Input("ctl-dataset-sel", "value"),
    Input("ctl-view-mode-sel", "value"),
    Input("ctl-value-graph-type", "value"),
    Input("ctl-trends-graph-type", "value"),
    Input("ctl-year-sel-start", "value"),
    Input("ctl-year-sel-end", "value"),
)
def update_data_value(selected_dataset, view_type, value_graph_type, trends_graph_type, start_year, end_year):
    selected_df = datasets[selected_dataset]
    filtered_df = selected_df[(selected_df['year'] >= start_year) & (selected_df['year'] <= end_year)]

    graph_func_map = {
        ('housing_data', 'general'): general_housing_graph,
        ('housing_data', 'compose'): compose_housing_graph,
        ('travel_data', 'general'): general_travel_graph,
        ('travel_data', 'compose'): compose_travel_graph,
        ('lm_data', 'general'): general_lm_graph,
        ('lm_data', 'compose'): compose_lm_graph,
    }

    if (key := (selected_dataset, view_type)) in graph_func_map:
        return graph_func_map[key](filtered_df, value_graph_type, trends_graph_type)


if __name__ == "__main__":
    app.run_server(debug=False)
