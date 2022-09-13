# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 09:45:06 2022

@author: cflorelu
"""
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
import plotly.express as px

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Señal Alertas"
server = app.server

df_final = pd.read_csv("data/df_final.csv")

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
            
            html.P("País : ", className="control_label"),
            dcc.Dropdown(df_final["pais"].unique(),
                         id ='input_select',
                         multi=True)],
            
            className="pretty_container four columns",
            id="cross-filter-options"
            ),
        
        #Barra de indicadores
        html.Div([
            
            html.Div([
                html.Div([html.H6(id="n_signal"), html.P("No. de señales")], id="number_signal", className="mini_container"),
                html.Div([html.H6(id="n_estables"), html.P("Estables")], id="estables", className="mini_container"),
                html.Div([html.H6(id="n_revision"), html.P("Revisión")], id="revision", className="mini_container")
                    ],
                id="info-container",
                className="row container-display"
                    ),
            
            #Visualizaciones
            html.Div([
                dcc.Graph(id = 'fig'),
                dcc.Graph(id = 'fig_1')],
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
def update_fig_0(selection):

    title = 'None'
    if selection:
        
        title = selection
        
    fig = go.Figure()
        
    tmp = df_final.groupby(["pais","linea","segmento","status_alerta"], as_index = False).count().iloc[:,:5]
    tmp["x"] = tmp['pais'] + "|" + tmp['linea'].astype(str) + "|" + tmp['segmento'].astype(str)
    tmp = tmp.iloc[:,[5,3,4]]
    tmp.columns = ["x","status_alerta","y"]
    tmp = tmp[tmp.stack().str.contains('|'.join(title)).any(level=0)]
    
    fig = px.bar(tmp,
                 x="x",
                 y="y",
                 color="status_alerta",
                 color_discrete_sequence=["green", "yellow", "red"],
                 title="Detalle General : País | Línea | Segmento")
    fig.show()

    return fig

@app.callback(
    Output(component_id = 'fig_1',
           component_property = 'figure'),
    Input(component_id = 'input_select',
           component_property = 'value')
     )
def update_fig_1(selection):

    title = 'None'
    if selection:
        
        title = selection
        
    fig = go.Figure()
        
    fig = px.scatter(
        df_final[df_final.stack().str.contains('|'.join(title)).any(level=0)],
        x="status_completitud",
        y="status_outlier", 
        color="status_alerta",
        color_discrete_sequence=["green", "red", "yellow"],
        size='status_cu', 
        hover_data=['pais'],
        title="Detalle Indicadores : Completitud | Outlier | N° Casos Uso")

    return fig


app.run_server(debug=True, use_reloader=False)
