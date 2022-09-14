# -*- coding: utf-8 -*-
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

#import plotly.io as pio
#pio.renderers.default='browser'

#Load data
df = pd.read_csv("data/df_final.csv")

app = dash.Dash( __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}] )
app.title = "Señal Alertas"
server = app.server

# Create app layout
app.layout = html.Div([
    
    html.Div([
        
        #Left side : Filter boxes
        html.Div([
            html.P("País : ", className="control_label"),
            dcc.RadioItems(
                id="input_country",
                options=[
                    {"label": "ARG ", "value": "Argentina"},
                    {"label": "BRA ", "value": "Brasil"},
                    {"label": "MEX ", "value": "México"}],
                value="Argentina",
                labelStyle={"display": "inline-block"},
                            className="dcc_control",
                ),
            html.P("Listado de señales :", className="control_label"),
            dcc.Dropdown(df["signal"].unique(),
                         id ='list_signal',
                         multi=True)
            ],
            className="pretty_container four columns",
            id="cross-filter-options"
            ),
        
        #Right side : 
        html.Div([
            #Indicator Boxes
            html.Div([
                
                html.Div([html.H6(id="n_signal"), html.P("No. de señales")],
                         id="number_signal",
                         className="mini_container"),
                html.Div([html.H6(id="n_estables"), html.P("Estables")],
                         id="estables",
                         className="mini_container"),
                html.Div([html.H6(id="n_revision"), html.P("Revisión")],
                         id="revision",
                         className="mini_container")
                
                ],
                id="info-container",
                className="row container-display"
                    ),
            
            #Views : graphs and tables.
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

# Helper functions
def filter_dataframe(df, input_country, list_signal):
    dff = df[ (df["pais"].isin([input_country])) 
            & (df.stack().str.contains('|'.join(list_signal)).any(level=0)) ]
    return dff

# Create callbacks

# Selectors -> n_signals text
@app.callback(
    Output("n_signal", "children"),
    [
     Input("input_country", "value"),
     Input("list_signal", "value")
    ],
)
def update_n_signal(input_country, list_signal):

    dff = filter_dataframe(df, input_country, list_signal)
    return dff.shape[0]

# Selectors -> n_estables text
@app.callback(
    Output("n_estables", "children"),
    [
     Input("input_country", "value"),
     Input("list_signal", "value")
    ],
)
def update_n_estables(input_country, list_signal):
    dff = filter_dataframe(df, input_country, list_signal)
    return dff[dff["status_alerta"] == 'estable'].shape[0]

# Main graph -> graph bar
@app.callback(
    Output(component_id = 'fig',
           component_property = 'figure'),
    [
     Input("input_country", "value"),
     Input("list_signal", "value")
    ])
def update_fig_0(input_country, list_signal):

    dff = filter_dataframe(df, input_country, list_signal)
    
    fig = go.Figure()

    tmp = dff.groupby(["pais","linea","segmento","status_alerta"], as_index = False).count().iloc[:,:5]
    tmp["x"] = tmp['pais'] + "|" + tmp['linea'].astype(str) + "|" + tmp['segmento'].astype(str)
    tmp = tmp.iloc[:,[5,3,4]]
    tmp.columns = ["x","status_alerta","y"]
    
    fig = px.bar(tmp,
                 x="x",
                 y="y",
                 color="status_alerta",
                 color_discrete_sequence=["green", "yellow", "red"],
                 title="Detalle General : País | Línea | Segmento")
    fig.show()

    return fig

# Main graph -> graph scatter
@app.callback(
    Output(component_id = 'fig_1',
           component_property = 'figure'),
    [
     Input('input_country', 'value'),
     Input("list_signal", "value")
    ])
def update_fig_1(input_country, list_signal):

    dff = filter_dataframe(df, input_country,list_signal)    

    fig = go.Figure()
        
    fig = px.scatter(
        dff,
        x="status_completitud",
        y="status_outlier", 
        color="status_alerta",
        color_discrete_sequence=["green", "red", "yellow"],
        size='status_cu', 
        hover_data=['pais'],
        title="Detalle Indicadores : Completitud | Outlier | N° Casos Uso")

    return fig

# Main
if __name__ == "__main__":
    app.run_server(debug=True, 
                   use_reloader=False)
