# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 09:45:06 2022

@author: cflorelu
"""

# Import required libraries
import pickle
import copy
import pathlib
import urllib.request
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Señal Alertas"
server = app.server

#Load data
df_day = pd.read_csv("data/df_day.csv")
df_day["signal"] = df_day["llave_comparativa"].str.split("|",expand=True).iloc[:,0]

df_missing_groups = pd.read_csv("data/df_missing_groups.csv")

signals = list(set(df_day["signal"]))

df_outlier = pd.read_csv("data/df_outlier.csv").iloc[:,1:]

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview")

# Create app layout
app.layout = html.Div([
    
    html.Div([
        #Barra de filtros
        html.Div([
            
            html.P("Selección de señales : ", className="control_label"),
            dcc.Dropdown(signals, id ='input_select',multi=True)],
            
            className="pretty_container four columns",
            id="cross-filter-options"
            ),
        
        #Barra de indicadores
        html.Div([
            
            html.Div([
                html.Div([html.H6(id="well_text"), 
                          html.P("No. de señales")],
                         id="wells",
                         className="mini_container"),
                html.Div([html.H6(id="gasText"),
                          html.P("Gas")],
                         id="gas",
                         className="mini_container"),
                html.Div([html.H6(id="oilText"),
                          html.P("Oil")],
                         id="oil",
                         className="mini_container"),
                
                html.Div([html.H6(id="waterText"),
                          html.P("Water")],
                         id="water",
                         className="mini_container")],
                id="info-container",
                className="row container-display"
                    ),
            
            #Visualizaciones
            html.Div([
                dcc.Graph(id = 'fig'),
                dcc.Graph(id='fig_table')],
                id="countGraphContainer",
                className="pretty_container")],
            id="right-column",
            className="eight columns")
        ],
        className="row flex-display"
        )
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"}
    )

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


app.run_server(debug=True, use_reloader=False)
