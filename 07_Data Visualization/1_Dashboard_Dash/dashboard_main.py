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

#Scripts de apoyo.
from utils.controls import COUNTRY

#Bases Output (ARG_Dask_signals_process.py)

df_day = pd.read_csv("data/df_day.csv")
df_day["signal"] = df_day["llave_comparativa"].str.split("|",expand=True).iloc[:,0]

df_missing_groups = pd.read_csv("data/df_missing_groups.csv")

signals = list(set(df_day["signal"]))

df_outlier = pd.read_csv("data/df_outlier.csv").iloc[:,1:]

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)

# Create controls
country_options = [ {"label": str(COUNTRY[county]), "value": str(county)} for county in COUNTRY ]

app.layout = html.Div([
    dcc.Dropdown(signals, id ='input_select',multi=True),
    dcc.Graph(id = 'fig'),
    dcc.Graph(id='fig_table')
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
        
    df_box = df_day[df_day.stack().str.contains('|'.join(title)).any(level=0)]

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

@app.callback(
    Output(component_id = 'fig_table',
           component_property = 'figure'),
    Input(component_id = 'input_select',
           component_property = 'value')
     )
def update_table(selection):

    title = 'None'
    if selection:
        
        title = selection
        
    fig = go.Figure()
    
    df_outlier_ = df_outlier[df_outlier.stack().str.contains('|'.join(title)).any(level=0)]

    trace_0 = go.Figure(data=[go.Table(
        header=dict(values=list(df_outlier_.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df_outlier_.señal, df_outlier_.grado_acero, df_outlier_.velocidad_linea, df_outlier_.ancho_slab,
                           df_outlier_.dia, df_outlier_.status_outlier, df_outlier_.pct_comparativo_mayo22],
                   fill_color='lavender',
                   align='left'))
    ])

    layout_0 = go.Layout(legend = {"x":.9,"y":.5},  margin=dict(l=20, r=20, t=20, b=20),
                         height = 4400,
                         showlegend = False,
                         paper_bgcolor='rgb(243, 243, 243)',
                         template = 'ggplot2',
                         plot_bgcolor='rgb(243, 243, 243)')

    fig = go.Figure(data = trace_0,
                          layout = layout_0)

    return fig


app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter


#3 inputs actualicen los datos
#hacer prueba poniendo gráficas en funciones


