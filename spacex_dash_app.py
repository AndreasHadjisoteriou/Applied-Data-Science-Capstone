# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',  # Unique identifier for this dropdown component
                                    options=[
                                    {'label': 'All Sites', 'value': 'ALL'},  # Default option for all sites
                                    {'label': 'Launch Site 1', 'value': 'CCAFS LC-40'},  # Add more launch sites here
                                    {'label': 'Launch Site 2', 'value': 'VAFB SLC-4E'},
                                    {'label': 'Launch Site 3', 'value': 'KSC LC-39A'},
                                    {'label': 'Launch Site 4', 'value': 'CCAFS SLC-40'}
                                    ],
                                    value='ALL',  # Default selected value (All Sites)
                                    placeholder="Select a Launch Site here",  # Placeholder text
                                    searchable=True  # Allows users to search for launch sites
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',  # Unique identifier for this RangeSlider component
                                    min=0,  # Minimum payload value (0 Kg)
                                    max=10000,  # Maximum payload value (10,000 Kg)
                                    step=1000,  # Interval between values (1,000 Kg)
                                    value=[min_payload, max_payload],  # Initial selected payload range
                                    marks={0: '0 Kg', 10000: '10,000 Kg'},  # Labels for the slider endpoints
                                ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Filter the DataFrame for all launch sites
        filtered_df = spacex_df
        # Calculate the total success count
        total_success_count = filtered_df[filtered_df['class'] == 1]['class'].count()
        total_failure_count = filtered_df[filtered_df['class'] == 0]['class'].count()
        # Create a pie chart
        fig = px.pie(
            values=[total_success_count, total_failure_count],
            names=['Success', 'Failure'],
            title='Total Launch Success Rate for All Sites'
        )
    else:
        # Filter the DataFrame for the selected launch site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        # Calculate the success and failure counts for the selected site
        success_count = (filtered_df['class'] == 1).sum()
        failure_count = (filtered_df['class'] == 0).sum()
        # Create a pie chart
        fig = px.pie(
            values=[success_count, failure_count],
            names=['Success', 'Failure'],
            title=f'Launch Success Rate for {selected_site}'
        )

    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        # Filter the DataFrame for all launch sites
        filtered_df = spacex_df
    else:
        # Filter the DataFrame for the selected launch site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
    
    # Filter the DataFrame based on the selected payload range
    filtered_df = filtered_df[
        (filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
        (filtered_df['Payload Mass (kg)'] <= payload_range[1])
    ]

    # Create a scatter plot
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=f'Scatter Plot of Payload vs. Launch Outcome for {selected_site if selected_site != "ALL" else "All Sites"}'
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
