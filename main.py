import json
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load the data
with open('pp3-4_2566_province.json', 'r', encoding='utf-8') as f:
    student_data = json.load(f)

with open('thailand.json', 'r', encoding='utf-8') as f:
    thailand_geojson = json.load(f)

# Convert the student data into a DataFrame
df = pd.DataFrame(student_data)

# Create the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Number of Students Graduated in 2566 (2023)"),
    dcc.Dropdown(
        id='province-dropdown',
        options=[{'label': province, 'value': province} for province in df['schools_province'].unique()],
        value=df['schools_province'].unique(),
        multi=True
    ),
    dcc.Graph(id='map-graph'),
    dcc.Graph(id='bar-graph')
])

@app.callback(
    [Output('map-graph', 'figure'),
     Output('bar-graph', 'figure')],
    [Input('province-dropdown', 'value')]
)
def update_graphs(selected_provinces):
    if not selected_provinces:
        selected_provinces = df['schools_province'].unique()
    
    filtered_df = df[df['schools_province'].isin(selected_provinces)]
    
    map_fig = px.choropleth_mapbox(
        filtered_df, 
        geojson=thailand_geojson, 
        locations='schools_province', 
        featureidkey='properties.name', 
        color='totalstd',
        mapbox_style="carto-positron",
        zoom=5, 
        center={"lat": 13.736717, "lon": 100.523186},
        opacity=0.5,
        labels={'totalstd': 'Total Students'}
    )
    map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    bar_fig = px.bar(
        filtered_df.melt(id_vars=['schools_province'], value_vars=['totalmale', 'totalfemale'], var_name='Gender', value_name='Count'),
        x='schools_province', y='Count', color='Gender', barmode='group'
    )
    
    return map_fig, bar_fig

if __name__ == '__main__':
    app.run_server(debug=True)
