# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 20:24:43 2022

@author: cflorelu
"""

import plotly.graph_objects as go # or plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash import Output, Input, dash_table

import plotly.graph_objects as go

#Bases Output (ARG_Dask_signals_process.py)

df_day = pd.read_csv("data/df_day.csv")
df_day["signal"] = df_day["llave_comparativa"].str.split("|",expand=True).iloc[:,0]

df_missing_groups = pd.read_csv("data/df_missing_groups.csv")
df_outlier = pd.read_csv("data/df_outlier.csv")

signals = list(set(df_day["signal"]))

app = dash.Dash()
app.layout = html.Div([
    dcc.Dropdown(signals, id ='input_select'),
    dcc.Graph(id = 'fig')
])

@app.callback(
    Output(component_id = 'fig',
           component_property = 'figure'),
    Input(component_id = 'input_select',
           component_property = 'value')
     )
def update_layouts(selection):

    title = 'None'
    if selection:
        
        title = selection
        
    fig = go.Figure()

    df_box = df_day[df_day["llave_comparativa"].str.contains(title)]

    fig.add_trace(go.Box(
        x = df_box["llave_comparativa"],
        y = df_box["value"],
        name='kale',
        boxpoints='all',
        jitter=0.5,
        whiskerwidth=0.2,
        marker_size=2,
        line_width=1)
        )
    
    return fig

app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter