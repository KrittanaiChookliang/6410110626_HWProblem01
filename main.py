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