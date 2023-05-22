# Import packages
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import glob
import os
from dash.dependencies import Input, Output
import pytest
from dash.testing.application_runners import import_app
from dash.testing.browser import Browser


folder_path = "/Users/onkar/Desktop/Quantium Virtual Program/quantium-virtual-program/data"  # Replace with the actual folder path where the CSV files are located
file_pattern = "*.csv"

# Construct the full file paths by joining the folder path with the file pattern
file_paths = glob.glob(os.path.join(folder_path, file_pattern))
data_frames = []

for file_path in file_paths:
    df = pd.read_csv(file_path)
    data_frames.append(df)

combined_df = pd.concat(data_frames, ignore_index=True)

combined_df = combined_df[combined_df['product'] == 'pink morsel']

combined_df['sales'] = combined_df['price'].str.replace('$', '').astype(float) * combined_df['quantity']
combined_df = combined_df.drop(['product','price', 'quantity'], axis=1)

# print(combined_df)

# Save the merged data frame to a new CSV file
output_file = "/Users/onkar/Desktop/Quantium Virtual Program/quantium-virtual-program/output.csv"  # Replace with the desired output file path
combined_df.to_csv(output_file, index=False)


# Create the Dash app
app = Dash(__name__)

# Set up the layout
app.layout = html.Div(children=[
    html.H1(children='Sales Visualization', style={'text-align': 'center', 'margin-top': '30px', 'color': '#FF0000'}),
    html.H2(children='Filter by Region', style={'text-align': 'center', 'margin-top': '20px', 'color': 'blue'}),

    dcc.RadioItems(
        id='region-filter',
        options=[
            {'label': 'North', 'value': 'north'},
            {'label': 'East', 'value': 'east'},
            {'label': 'South', 'value': 'south'},
            {'label': 'West', 'value': 'west'},
            {'label': 'All', 'value': 'all'}
        ],
        value='all',
        labelStyle={'display': 'inline-block', 'margin': '0 10px'}
    ),

    dcc.Graph(
        id='sales-chart',
        style={'height': '400px', 'margin-top': '30px'}
    )
], style={'width': '50%', 'margin': 'auto', 'font-family': 'Arial, sans-serif', 'background-color': '#f9f9f9', 'padding': '20px', 'border': '1px solid #ccc'})

# Define the callback function to update the chart based on the region selection
@app.callback(
    Output('sales-chart', 'figure'),
    [Input('region-filter', 'value')]
)
def update_chart(region):
    if region == 'all':
        df_filtered = combined_df
    else:
        df_filtered = combined_df[combined_df['region'] == region]

    df_filtered = df_filtered.sort_values('date')

    fig = px.line(df_filtered, x='date', y='sales')

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


# Load the Dash app
app = import_app("app")

# Create a browser instance
browser = Browser(app)

def test_header_present():
    # Start the app in the browser
    browser.server_url = "http://localhost:8050/"
    browser.reload()

    # Find the header element
    header_element = browser.wait_for_element("#header")

    # Assert that the header is present
    assert header_element.text == "Sales Visualization"

def test_visualization_present():
    # Start the app in the browser
    browser.server_url = "http://localhost:8050/"
    browser.reload()

    # Find the visualization element
    visualization_element = browser.wait_for_element("#sales-chart")

    # Assert that the visualization is present
    assert visualization_element is not None

def test_region_picker_present():
    # Start the app in the browser
    browser.server_url = "http://localhost:8050/"
    browser.reload()

    # Find the region picker element
    region_picker_element = browser.wait_for_element("#region-filter")

    # Assert that the region picker is present
    assert region_picker_element is not None

# Execute the test suite
if __name__ == "__main__":
    pytest.main([__file__])