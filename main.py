import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import json

# ตรวจสอบเส้นทางไปยังไฟล์ JSON
file_path = 'pp3-4_2566_province.json'
geojson_path = 'thailand-provinces.json'  # เพิ่มเส้นทางไปยังไฟล์ GeoJSON

# อ่านข้อมูลจากไฟล์ JSON
df = pd.read_json(file_path)

# อ่านข้อมูลจากไฟล์ GeoJSON
with open(geojson_path) as f:
    geojson = json.load(f)

# สร้างคอลัมน์ใหม่สำหรับการแสดงข้อมูลในแผนที่
df['province'] = df['schools_province']
df['totalmale'] = df['totalmale'].astype(int)
df['totalfemale'] = df['totalfemale'].astype(int)
df['totalstd'] = df['totalstd'].astype(int)

# สร้างแอป Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1('Dashboard จำนวนนักเรียนที่จบปี 2566 แยกตามจังหวัดและเพศ'),
    dcc.Dropdown(
        id='gender-dropdown',
        options=[
            {'label': 'ทั้งหมด', 'value': 'totalstd'},
            {'label': 'เพศชาย', 'value': 'totalmale'},
            {'label': 'เพศหญิง', 'value': 'totalfemale'}
        ],
        value='totalstd',
        clearable=False
    ),
    dcc.Graph(id='map-graph'),
    dcc.Graph(id='bar-graph')
])

@app.callback(
    [Output('map-graph', 'figure'),
     Output('bar-graph', 'figure')],
    [Input('gender-dropdown', 'value')]
)
def update_graph(selected_gender):
    # สร้างแผนที่
    map_fig = px.choropleth(
        df,
        geojson=geojson,
        locations='province',
        featureidkey='properties.NAME_1',  # ระบุคีย์ที่ใช้สำหรับการจับคู่ข้อมูลใน GeoJSON
        color=selected_gender,
        hover_name='province',
        hover_data=['totalmale', 'totalfemale', 'totalstd'],
        color_continuous_scale='Viridis',
        labels={'totalmale': 'เพศชาย', 'totalfemale': 'เพศหญิง', 'totalstd': 'ทั้งหมด'}
    )
    map_fig.update_geos(fitbounds="locations", visible=False)

    # สร้างแผนภูมิแท่ง
    bar_fig = px.bar(
        df,
        x='province',
        y=selected_gender,
        hover_data=['totalmale', 'totalfemale', 'totalstd'],
        labels={'province': 'จังหวัด', 'totalmale': 'เพศชาย', 'totalfemale': 'เพศหญิง', 'totalstd': 'ทั้งหมด'}
    )
    bar_fig.update_layout(xaxis={'categoryorder': 'total descending'})

    return map_fig, bar_fig

if __name__ == '__main__':
    app.run_server(debug=True)