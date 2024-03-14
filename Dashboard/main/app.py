from dash import Dash, dcc, Input, Output, Patch, html
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash import dcc, html
import plotly.graph_objects as go
import numpy as np
from io import StringIO
import glob
import warnings

# Suppress specific deprecation warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# Path to your dataset directory, adjust as needed
dataset_path = 'HPC_Project/Dashboard/main/datasets/'

# List all CSV files in the directory
csv_files = glob.glob(dataset_path + '*.csv')

# Determine the number of files
num_files = len(csv_files)


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
dims = ["opti_flag_id", "vecto_flag_id", "x_tbs", "y_tbs","z_tbs","n_threads","rank"]


df = pd.read_csv(dataset_path+'data1.csv')

def prepare_data(df):
    # Define mappings
    opti_mapping = {1: '0fast', 2: 'O2', 3: 'O3'}
    vecto_mapping = {1: 'sse', 2: 'avx', 3: 'avx2', 4: 'avx512'}

    # Create new columns with string representations
    df['Opti_flag'] = df['opti_flag_id'].map(opti_mapping)
    df['Vecto_flag'] = df['vecto_flag_id'].map(vecto_mapping)

    # Insert 'Opti_flag' at the desired position (2nd position, so index=1)
    df.insert(1, 'Opti_flag', df.pop('Opti_flag'))

    # Insert 'Vecto_flag' at the desired position (4th position, so index=3)
    df.insert(3, 'Vecto_flag', df.pop('Vecto_flag'))



    # Apply log2 transformation
    df['x_tbs'] = np.log2(df['x_tbs'])
    df['y_tbs'] = np.log2(df['y_tbs'])
    df['z_tbs'] = np.log2(df['z_tbs'])

prepare_data(df)


column_defs = [
    {"field": "Opti_flag", "sortable": True},
    {"field": "opti_flag_id", "sortable": False},
    {"field": "Vecto_flag", "sortable": True},
    {"field": "vecto_flag_id", "sortable": False},
    {"field": "x_tbs", "sortable": True},
    {"field": "y_tbs", "sortable": True},
    {"field": "z_tbs", "sortable": True},
    {"field": "n_threads", "sortable": True},
    {"field": "rank", "sortable": True},
]

color_scale_options = [
    {'label': 'Tealrose', 'value': 'Tealrose'},
    {'label': 'Tropic', 'value': 'Tropic'},
    {'label': 'Earth', 'value': 'Earth'},
    {'label': 'Electric', 'value': 'Electric'},
    # Add more color scales as desired
]


# Prepare data for the dimensions of the Parcoords
dimensions = [
    {"label": "Optimization Flag", "values": df["opti_flag_id"], "tickvals": [1, 2, 3], "ticktext": df["Opti_flag"]},
    {"label": "Vectorization Flag", "values": df["vecto_flag_id"], "tickvals": [1, 2, 3, 4], "ticktext": df["Vecto_flag"]},
    {"range": [min(df["x_tbs"]), max(df["x_tbs"])], "label": "X TBS", "values": df["x_tbs"]},
    {"range": [min(df["y_tbs"]), max(df["y_tbs"])], "label": "Y TBS", "values": df["y_tbs"]},
    {"range": [min(df["z_tbs"]), max(df["z_tbs"])], "label": "Z TBS", "values": df["z_tbs"]},
    {"range": [min(df["n_threads"]), max(df["n_threads"])], "label": "Number of Threads", "values": df["n_threads"]},
    {"range": [min(df["rank"]), max(df["rank"])], "label": "Rank", "values": df["rank"], "constraintrange": [0.5]}  # This is to demonstrate how to set a specific filtering range; adjust as needed
]

# Create the Parcoords figure
fig = go.Figure(data=
    go.Parcoords(
        line=dict(color=df["rank"], colorscale="Tealrose", showscale=True, cmin=0, cmax=1),
        dimensions=dimensions
    )
)


# Parameters for bar charts
parameters = ["Opti_flag", "Vecto_flag", "x_tbs", "y_tbs", "z_tbs", "n_threads"]

slider_container = html.Div(
    children=[  # Enclose the children components in a list
        html.Label("Select Dataset:"),
        dcc.Slider(
            id='dataset-slider',
            min=1,
            max=num_files,  # Use the dynamically determined number of files
            value=1,  # Default value
            marks={i: f'Data {i}' for i in range(1, num_files + 1)},  # Ensure the range starts at 1 if your datasets are named starting from 1
            step=1,
        ),
    ],
    id='slider-container',  # Now correctly recognized as a named argument for the Div
)

app.layout = dbc.Container([
    html.Div(style={'margin': '80px'}),
    dcc.Store(id='current-dataset'),
    html.H2("Filtering a Datatable with Parallel Coordinates"),
    html.Div(style={'margin': '40px'}),
    dcc.Dropdown(
        id='colorscale-dropdown',
        options=color_scale_options,  # Assumes color_scale_options is defined
        value='Tealrose',  # Default value
        clearable=False,
    ),
    slider_container,
    dcc.Graph(id="my-graph"),
    dag.AgGrid(
        id="table",
        columnDefs=[{"field": i} for i in df.columns],  # Assumes df is defined
        defaultColDef={
            "sortable": True,  # Enable sorting for all columns
            "minWidth": 120,
            "filter": True,  # Optional: Enable filtering for all columns
            "resizable": True,  # Optional: Allow column resizing
        },
        columnSize="sizeToFit",
    ),
    dcc.Store(id="activefilters", data={}),

    # Spacing and separator
    html.Div(style={'margin': '100px'}),  # Adjust the margin value as needed for spacing
    html.Hr(),  # Horizontal line as a separator

    html.H2("Parameter Distributions"),  # Section title for bar charts
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar-chart-Opti_flag'), width=6),
        dbc.Col(dcc.Graph(id='bar-chart-Vecto_flag'), width=6),
    ]),

    # Row for side-by-side bar charts for specific parameters
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar-chart-x_tbs'), width=4),
        dbc.Col(dcc.Graph(id='bar-chart-y_tbs'), width=4),
        dbc.Col(dcc.Graph(id='bar-chart-z_tbs'), width=4),
    ]),
    
    # Additional bar charts for other parameters (if any)
    html.Div([
        dcc.Graph(id='bar-chart-n_threads')
    ]),
])


def load_dataset_from_slider(slider_value):
    """
    Loads a dataset based on the provided slider value.
    
    Parameters:
    - slider_value: The value of the slider, used to determine which dataset to load.
    
    Returns:
    - A pandas DataFrame containing the data from the selected dataset.
    """
    
    # Define the base path to your datasets and the filename pattern
    base_path = "HPC_Project/Dashboard/main/datasets/"
    filename_pattern = "data{}.csv"
    
    # Construct the full filepath based on the slider value
    filepath = base_path + filename_pattern.format(slider_value)
    
    # Load the dataset into a DataFrame
    df = pd.read_csv(filepath)
    prepare_data(df)
    
    return df


@app.callback(
    Output('current-dataset', 'data'),
    [Input('dataset-slider', 'value')]
)
def load_dataset(slider_value):
    # Assuming a function `load_dataset_from_slider` that returns a DataFrame based on the slider value
    df = load_dataset_from_slider(slider_value)
    return df.to_json(date_format='iso', orient='split')




@app.callback(
    Output("table", "rowData"),
    [Input("current-dataset", "data"), Input("activefilters", "data")]
)
def update_table(dataset_json, active_filters):
    # Convert the dataset from JSON to a DataFrame
    df = pd.read_json(dataset_json, orient='split')
    
    # Proceed with filtering based on 'active_filters'
    if active_filters:
        dff = df.copy()
        for col in active_filters:
            if active_filters[col]:
                rng = active_filters[col][0]
                if isinstance(rng[0], list):
                    # If multiple choices, combine DataFrame parts
                    dff3 = pd.DataFrame(columns=df.columns)
                    for i in rng:
                        dff2 = dff[dff[col].between(i[0], i[1])]
                        dff3 = pd.concat([dff3, dff2])
                    dff = dff3
                else:
                    # If one choice
                    dff = dff[dff[col].between(rng[0], rng[1])]
        return dff.to_dict("records")
    return df.to_dict("records")




@app.callback(
    Output("activefilters", "data"),
    Input("my-graph", "restyleData"),
)
def updateFilters(data):
    if data:
        key = list(data[0].keys())[0]
        col = dims[int(key.split("[")[1].split("]")[0])]
        newData = Patch()
        newData[col] = data[0][key]
        return newData
    return {}


@app.callback(
    Output('my-graph', 'figure'),
    [Input('current-dataset', 'data'),
     Input('colorscale-dropdown', 'value')]
)
def update_figure(dataset_json, selected_colorscale):
    # Convert the dataset from JSON to a DataFrame
    df = pd.read_json(dataset_json, orient='split')

    # Prepare dimensions for the Parcoords
    dimensions = [
        {"label": "Optimization Flag", "values": df["opti_flag_id"], "tickvals": [1, 2, 3], "ticktext": df["Opti_flag"]},
        {"label": "Vectorization Flag", "values": df["vecto_flag_id"], "tickvals": [1, 2, 3, 4], "ticktext": df["Vecto_flag"]},
        {"label": "X TBS", "values": df["x_tbs"]},
        {"label": "Y TBS", "values": df["y_tbs"]},
        {"label": "Z TBS", "values": df["z_tbs"]},
        {"label": "Number of Threads", "values": df["n_threads"]},
        {"label": "Rank", "values": df["rank"]}
    ]

    # Create the Parcoords figure using Graph Objects
    fig = go.Figure(data=go.Parcoords(
        line=dict(color=df["rank"], colorscale=selected_colorscale, showscale = True, cmin=df["rank"].min(), cmax=df["rank"].max()),
        dimensions=dimensions
    ))

    return fig



@app.callback(
    [Output(f'bar-chart-{param}', 'figure') for param in parameters],
    [Input('table', 'rowData')]
)
def update_bar_charts(rowData):
    # Convert rowData (which is a list of dicts) back to a DataFrame
    dff = pd.DataFrame(rowData)
    
    figures = []
    for param in parameters:
        # For each parameter, generate a sorted bar chart based on 'rank'
        if param in dff:
            sorted_df = dff.sort_values(by=["rank", param])
            fig = px.bar(sorted_df, x=param, y='rank', text='rank',color_discrete_sequence=['#005F60'])
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            fig.update_layout(uniformtext_minsize=8)
            figures.append(fig)
        else:
            # Append an empty figure if the parameter doesn't exist in the data
            figures.append(px.bar())

    return figures


if __name__ == "__main__":
    app.run_server(debug=True)