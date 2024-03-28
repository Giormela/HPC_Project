from dash import Dash, dcc, Input, Output, Patch, html, State
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
import os

# Suppress specific deprecation warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# Path to your dataset directory, adjust as needed
# Print the current working directory
dataset_path = 'Dashboard/main/datasets/dataset_linear/'

# Define your dataset directories for selection
dataset_directories = {
    'Linear Dataset': 'Dashboard/main/datasets/dataset_linear/',
    'Hyperbolic Dataset': 'Dashboard/main/datasets/dataset_hyperbolic/',
    'Relu dataset': 'Dashboard/main/datasets/dataset_relu/',
    'Performance Dataset': 'Dashboard/main/datasets/dataset_performance/',
    # Add more directories here as needed
}

# Modal Trigger Button
open_modal_btn = dbc.Button(id="open-modal-btn", className="mb-3", color="primary")

# Modal with Directory Selection
select_directory_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Select Dataset Directory")),
        dbc.ModalBody(
            dcc.Dropdown(
                id='directory-dropdown',
                options=[{'label': k, 'value': v} for k, v in dataset_directories.items()],
                value=list(dataset_directories.values())[0],  # Default value is the first directory
            )
        ),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-modal-btn", className="ml-auto")
        ),
    ],
    id="modal",
    is_open=False,  # Modal is initially closed
)

# List all CSV files in the directory
csv_files = glob.glob(dataset_path + '*.csv')

# Determine the number of files
num_files = len(csv_files)


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
dims = ["opti_flag_id", "vecto_flag_id", "x_tbs", "y_tbs","z_tbs","n_threads","rank"]


df = pd.read_csv(dataset_path+'data0.csv')


# Ensure df is sorted by 'rank' for logical bar chart progression
df_sorted = df.sort_values(by='rank')

def prepare_data(df):
    # Define mappings
    opti_mapping = {0: 'O3', 1: '0fast'}
    vecto_mapping = {1: 'sse', 2: 'avx', 3: 'avx2', 4: 'avx512'}
    df['vecto_flag_id'] = df['vecto_flag_id'] +1
    # Create new columns with string representations
    df['Opti_flag'] = df['opti_flag_id'].map(opti_mapping)
    df['Vecto_flag'] = df['vecto_flag_id'].map(vecto_mapping)

    # Insert 'Opti_flag' at the desired position (2nd position, so index=1)
    df.insert(1, 'Opti_flag', df.pop('Opti_flag'))

    # Insert 'Vecto_flag' at the desired position (4th position, so index=3)
    df.insert(3, 'Vecto_flag', df.pop('Vecto_flag'))

    # Limit digit numbers
    df['rank'] = df['rank'].round(3)  # Round to  decimal places before passing to AG Grid


prepare_data(df)


# Initialize a dictionary to store avg ranks for each category
category_avg_ranks = {}

for category, pathh_pattern in dataset_directories.items():
    avg_ranks = []
    # Sorted to ensure files are processed in order
    for filepath in sorted(glob.glob(pathh_pattern+'*')):
        ddf = pd.read_csv(filepath)
        avg_rank = (ddf['rank'].sum())/len(ddf["rank"])
        avg_ranks.append(avg_rank)
    category_avg_ranks[category] = avg_ranks


# Initialize a dictionary to store max ranks for each category
category_max_ranks = {}

for category, path_pattern in dataset_directories.items():
    max_ranks = []
    # Sorted to ensure files are processed in order
    for filepath in sorted(glob.glob(path_pattern+'*')):
        dddf = pd.read_csv(filepath)
        max_rank = dddf['rank'].max()  # Calculate the maximum rank value
        max_ranks.append(max_rank)
    category_max_ranks[category] = max_ranks


figgg = go.Figure()

for category, avg_ranks in category_avg_ranks.items():
    iterations = list(range(1, len(avg_ranks) + 1))
    figgg.add_trace(go.Scatter(x=iterations, y=avg_ranks, mode='lines+markers', name=category))


# Update layout if necessary
figgg.update_layout(height=600, 
                    title_text="Average Gflops Value Across Iterations by Method",
                    xaxis_title = 'Iterations',
                    yaxis_title = 'Gflops',
                    legend_title = 'Methods'
                    )

# Initialize an empty figure for plotting max ranks
figg = go.Figure()

# Add a trace for each category's max ranks
for category, max_ranks in category_max_ranks.items():
    iterationss = list(range(1, len(max_ranks) + 1))
    figg.add_trace(go.Scatter(x=iterationss, y=max_ranks, mode='lines+markers', name=category))

# Customize the layout
figg.update_layout(
    height=600, 
    title_text="Maximum Gflops Value Across Iterations by Category",
    xaxis_title='Iterations',
    yaxis_title='Max Gflops',
    legend_title='Methods'
)


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
    {'label': 'Cividis', 'value': 'Cividis'},
    # Add more color scales as desired
]


# Prepare data for the dimensions of the Parcoords
dimensions = [
    {"label": "Optimization Flag", "values": df["opti_flag_id"], "tickvals": [0, 1, 2], "ticktext": df["Opti_flag"]},
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
        line=dict(color=df["rank"], colorscale="Tealrose", showscale=True, cmin=0, cmax=150),
        dimensions=dimensions
    )
)


# Parameters for bar charts
parameters = ["Opti_flag", "Vecto_flag", "x_tbs", "y_tbs", "z_tbs", "n_threads","rank"]

slider_container = html.Div(
    children=[  # Enclose the children components in a list
        html.Label("Select iteration :"),
        html.Div(style={'margin': '5px'}),
        dcc.Slider(
            id='dataset-slider',
            min=0,
            max=num_files-1,  # Use the dynamically determined number of files
            value=0,  # Default value
            marks={i: str(i) for i in range(num_files)},  # Ensure the range starts at 0 if your datasets are named starting from 0
            step=1,
        ),
    ],
    id='slider-container',  # Now correctly recognized as a named argument for the Div
)

app.layout = dbc.Container([
    html.Div(
        style={
            'display' : 'flex',
            'alignItems': 'center',  # Align items vertically
            'justifyContent': 'center',  # Center items horizontally
            'backgroundColor': '#005F60',
            'color': 'white',
            'padding': '10px',
            'position': 'fixed',
            'width': '100%',
            'top': 0,
            'left': 0,
            'zIndex': 9999,
            'boxShadow': '0px 4px 8px 0px rgba(0,0,0,0.2)'  # Adding shadow
        },
        children=[
            # Button aligned to the left
            html.Div(open_modal_btn, style={'position': 'absolute', 'left': '200px '}),
            
            # Title centered
            html.H1("HPC Ant colony Optimization", style={'textAlign': 'center'}),
            html.H4("Number of Ants: ", id='ants-count-display', style={'position' : 'absolute', 'right': '200px', 'color': 'white'})
            ]
    ),
    html.Div(style={'margin': '120px'}),
    dcc.Store(id='current-dataset'),
    html.Div(style={'margin': '40px'}),
    dcc.Store(id='current-dataset-directory'),
    select_directory_modal,
    html.Div(style={'margin': '100px'}),
    html.H2("Filtering Ants Paths with Parallel Coordinates"),
    html.Div(style={'margin': '20px'}),
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
    # Spacing and separator
    html.Div(style={'margin': '100px'}),  # Adjust the margin value as needed for spacing
    html.Hr(),  # Horizontal line as a separator
    html.H2("Ants ranking"),  # Section title for bar charts

    html.Div([
        dcc.Graph(id='bar-chart-rank')
    ]),

    html.Div(style={'margin': '100px'}),  # Adjust the margin value as needed for spacing
    html.Hr(),  # Horizontal line as a separator
    html.H2("Method comparison"), 

    dcc.Graph(
        id='category-plot',
        figure=figgg  # This is where you pass your figure to the Dash component
    ),
    dcc.Graph(
        id='category-plot',
        figure=figg  # This is where you pass your figure to the Dash component
    ),
    html.Div(style={'margin': '200px'}),
])

@app.callback(
    Output("open-modal-btn", "children"),
    [Input("directory-dropdown", "value")],  # Assuming this is the ID of your dropdown
)
def update_button_label(selected_directory):
    if selected_directory:
        # Assuming `dataset_directories` is a dict mapping labels to directory paths
        # and you want to display the label, not the actual path
        label = [label for label, path in dataset_directories.items() if path == selected_directory][0]
        return f"Change Directory: {label}"
    return "Change Directory"

@app.callback(
    Output('ants-count-display', 'children'),
    [Input('current-dataset', 'data')]
)
def update_ants_count_display(dataset_json):
    if dataset_json:
        df = pd.read_json(dataset_json, orient='split')
        ants_count = len(df)
        return f"Number of ants (paths): {ants_count}"
    return "Number of ants (paths): 0"



def load_dataset_from_slider(slider_value,directory):
    """
    Loads a dataset based on the provided slider value.
    
    Parameters:
    - slider_value: The value of the slider, used to determine which dataset to load.
    
    Returns:
    - A pandas DataFrame containing the data from the selected dataset.
    """
    
    # Define the base path to your datasets and the filename pattern
    base_path = dataset_path
    filename_pattern = "data{}.csv"
    
    # Construct the full filepath based on the slider value
    filepath = directory + filename_pattern.format(slider_value)
    
    # Load the dataset into a DataFrame
    df = pd.read_csv(filepath)
    prepare_data(df)
    
    return df

# Callback for opening the modal
@app.callback(
    Output("modal", "is_open"),
    [Input("open-modal-btn", "n_clicks"), Input("close-modal-btn", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Callback for setting the selected directory
@app.callback(
    Output('current-dataset-directory', 'data'),  # You need to add this dcc.Store component to your layout
    [Input('directory-dropdown', 'value')],
)
def update_directory(selected_directory):
    if not selected_directory:
        return 'Dashboard/main/datasets/dataset_linear/'
    return selected_directory


@app.callback(
    [Output('dataset-slider', 'max'),
     Output('dataset-slider', 'marks'),
     Output('dataset-slider', 'value')],
    [Input('current-dataset-directory', 'data')]
)
def update_slider(directory):
    # Assuming the directory contains only CSV files intended for use
    csv_files = glob.glob(os.path.join(directory, '*.csv'))
    num_files = len(csv_files)
    min=0,
    max=num_files-2,  # Use the dynamically determined number of files
    value=0,  # Default value
    marks={i: str(i) for i in range(num_files)},  # Ensure the range starts at 0 if your datasets are named starting from 0    
    step=1,
    # Reset slider value to 0 (default value) when directory changes
    return max[0], marks[0], 0

@app.callback(
    Output('current-dataset', 'data'),
    [Input('dataset-slider', 'value'),
     Input('current-dataset-directory', 'data')]
)
def load_dataset(slider_value,directory):
    # Assuming a function `load_dataset_from_slider` that returns a DataFrame based on the slider value
    df = load_dataset_from_slider(slider_value,directory)
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
        {"label": "Optimization Flag", "values": df["opti_flag_id"], "tickvals": [0, 1, 2], "ticktext": df["Opti_flag"]},
        {"label": "Vectorization Flag", "values": df["vecto_flag_id"], "tickvals": [1, 2, 3, 4], "ticktext": df["Vecto_flag"]},
        {"label": "X TBS", "values": df["x_tbs"]},
        {"label": "Y TBS", "values": df["y_tbs"]},
        {"label": "Z TBS", "values": df["z_tbs"]},
        {"label": "Number of Threads", "values": df["n_threads"]},
        {"label": "Gflops", "values": df["rank"]}
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
            sorted_df['rank_text'] = sorted_df['rank'].map('{:,.2f}'.format)
            if param == "rank":
                fig = px.bar(sorted_df, y='rank', text='rank',color="rank")
            else:
                fig = px.bar(sorted_df, x=param, y='rank', text='rank', color_discrete_sequence=['#005F60'])
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            fig.update_layout(uniformtext_minsize=8, yaxis_title = "Gflops")
            figures.append(fig)
            
        else:
            # Append an empty figure if the parameter doesn't exist in the data
            figures.append(px.bar())

        

    return figures


if __name__ == "__main__":
    app.run_server(debug=True)