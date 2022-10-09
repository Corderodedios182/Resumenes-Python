# -*- coding: utf-8 -*-

# import dash IO and graph objects
from dash.dependencies import Input, Output

# Plotly graph objects to render graph plots
import plotly.graph_objects as go
import plotly.express as px

# Import dash html, bootstrap components, and tables for datatables
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

import dash_html_components as html
from dash import dash_table
import dash_daq as daq

#import plotly.io as pio
#pio.renderers.default='browser'

#Data Processing
import pandas as pd
import numpy as np
from datetime import date
import datetime
from datetime import datetime, timedelta
import dask.dataframe as dd

#DataBases Master
ddf_signal = dd.read_csv("data/ddf_signal/*.csv").compute()
ddf_signal['Time'] = pd.to_datetime(ddf_signal['Time'])

#Filtros ddebbug
input_country = 'Argentina'
signal = "s4_drv_net_a_ea_seg12_torque_ref_C1074856020"

day = '2022-10-08'
grado_acero = 7546
app = dash.Dash( __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}] )
app.title = "Calidad de la señal"
server = app.server

####################
# Create app layout#
#################a###
app.layout = html.Div(
    children=[
        
        # Top Banner
        html.Div(className="study-browser-banner row",
                 children=[html.H2(className="h2-title", children="CALIDAD DE SEÑAL"),
                           html.Div(className="div-logo",children=html.Img(className="logo", src=app.get_asset_url("Ternium.png"))),
                           html.H2(className="h2-title-mobile", children="CALIDAD DE SEÑAL")
                           ]),
        
        # Body of the App
        html.Div(className="row app-body",
                 children=[

                     # User Controls
                     html.Div(
                         children=[html.Div(children=[html.Div(children=[html.H6("Selecciona una señal : "),
                                                                         dcc.Dropdown(ddf_signal.columns[1:-1],
                                                                                      id = "signal")]),

                                                      html.Div(children=[html.H6("Selecciona un día : "),
                                                                         dcc.DatePickerSingle(
                                                                                     id ='day',
                                                                                     min_date_allowed = datetime.today() + timedelta(days =-30),
                                                                                     max_date_allowed = datetime.today() ) ]),
                                                      
                                                      html.Div(children=[html.H6("Selecciona un grado de acero : "),
                                                                                                      dcc.Dropdown(ddf_signal["grado_acero"].unique(),
                                                                                                                   id = "grado_acero")]),

                                                      html.Div(children=[html.H6(" "),
                                                                         html.Button('Consultar datos de Señal : ', id='boton', n_clicks=0)]),

                                                      html.Div(children=[html.H6(' '),
                                                                         dcc.Loading(id="loading-1", type="default", children=html.Div(id="loading")),
                                                                         html.H6(' ')]),
                                                      
                                                      html.Div([
                                                          html.Div(
                                                              [html.H6(id="count"), html.P("Registros")],
                                                              className="mini_container"),
                                                          html.Div(
                                                              [html.H6(id="mean"), html.P("Promedio")],
                                                              className="mini_container"),
                                                          html.Div(
                                                              [html.H6(id="std"), html.P("Desviación Estandar")],
                                                              className="mini_container"),
                                                          html.Div(
                                                              [html.H6(id="min"), html.P("Mínimo")],
                                                              className="mini_container"),
                                                          html.Div(
                                                              [html.H6(id="max"), html.P("Máximo")],
                                                              className="mini_container"),
                                                          html.Div(
                                                              [html.H6(id="Q1"), html.P("Primer Quantile")],
                                                              className="mini_container"),
                                                          html.Div(
                                                              [html.H6(id="Q3"), html.P("Tercer Quantile")],
                                                              className="mini_container"),
                                                          html.Div(
                                                              [html.H6(id="vall_null"), html.P("Valores Nulos")],
                                                              className="mini_container")
                                                          ],
                                                          id="info-container",
                                                          className="row container-display"
                                                          ),
                                                      
                                                      html.Div(children=[html.Br(' '),
                                                                         html.H6("Selecciona un tipo de gráfico : "),
                                                                         dcc.Tabs(id="type_graph", children=[
                                                                         dcc.Tab(label='Histograma', value='histograma'),
                                                                         dcc.Tab(label='Señal en el tiempo', value='señal_tiempo'),
                                                                         dcc.Tab(label='Señal en el tiempo por grupos', value='señal_tiempo_grupos')])]),
                                                      
                         ])])]),
                    # Graph
                    html.Div([
                        dcc.Graph(id="plot"),
                        html.P("Detalle de la información :", className="control_label"),
                        html.Button("Download CSV", id="btn_csv"),
                        dcc.Download(id="download-dataframe-csv")
                        ],
                        id="countGraphContainer",
                        className="pretty_container")
                    ])

###################
# Helper functions#
###################
def get_data(signal = signal, day = day, days = 1, grado_acero = 0):
    
    inicio = datetime.strptime(str(day), '%Y-%m-%d') - timedelta(days= int(days))    
    fin =    datetime.strptime(str(day), '%Y-%m-%d') + timedelta(days= int(days))
    
    columns = ["Time","groupings","grado_acero",signal]
    
    if grado_acero != 0:
        return ddf_signal[(ddf_signal["Time"] >= inicio) &
                          (ddf_signal["Time"] <= fin) & 
                          (ddf_signal["grado_acero"] == grado_acero)].loc[:,columns]
    else: 
        return ddf_signal[(ddf_signal["Time"] >= inicio) & (ddf_signal["Time"] <= fin)].loc[:,columns]

##################
#Create callbacks#
##################

@app.callback(
    Output("plot", "figure"),
    [Input("signal", "value"),
     Input("type_graph", "value"),
     Input('day', 'date'),
     Input("grado_acero", "value")     ]
)
def update_grafico(signal, type_graph, day, grado_acero):
    """Muestra el tipo de gráfico a visualzar"""
    data = get_data(signal, day, grado_acero)
    data.columns = ["Time", "groupings", "grado_acero", "value"]
    
    mean = np.mean(data.value)
    std = np.std(data.value)
    
    q1 = np.quantile(data.value, .25)
    q3 = np.quantile(data.value, .75)
    
    if type_graph == 'histograma':
        bar_graph = px.histogram(data,
                                 x = "value",
                                 title = r"Histograma señal : {}".format(signal))
        
        bar_graph.add_vline(x = mean, line_dash = "dash", line_color = "red", annotation_text = "Promedio")
        bar_graph.add_vline(x = std, line_dash = "dash", line_color = "red", annotation_text = "std")
        
        bar_graph.add_vline(x = q1, line_dash = "dash", line_color = "red", annotation_text = "Q1")
        bar_graph.add_vline(x = q3, line_dash = "dash", line_color = "red", annotation_text = "Q3")
        
        return bar_graph
    elif type_graph == 'señal_tiempo':
        bar_line = px.line(data_frame = data,
                           x = data["Time"],
                           y = data["value"],
                           title = r"Serie de tiempo señal : {}".format(signal)) 
        return bar_line
    elif type_graph == 'señal_tiempo_grupos':
        scatter_graph = px.scatter(
            data,
            x = "Time",
            y = "value", 
            color = "grado_acero",
            title = r"Serie de tiempo grupos : Grado | Velocidad | Ancho : {}".format(signal))
        
        scatter_graph.update_traces(mode="markers+lines", hovertemplate=None)
        scatter_graph.update_layout(hovermode="x")
        
        return scatter_graph
    else:
        return {}

# Selectors -> counts
@app.callback(
    Output("count", "children"),
    [Input("signal", "value"), Input('day', 'date')])
def update_n_counts(signal, day):
    data = get_data(signal, day)
    return data.shape[0]

# Selectors -> mean
@app.callback(
    Output("mean", "children"),
    [Input("signal", "value"), Input('day', 'date')])
def update_mean(signal, day):
    data = get_data(signal, day)
    return round(np.mean(data.iloc[:,2]),1)

# Selectors -> std
@app.callback(
    Output("std", "children"),
    [Input("signal", "value"), Input('day', 'date')])
def update_std(signal, day):
    data = get_data(signal, day)
    return round(np.std(data.iloc[:,2]),1)

# Selectors -> min
@app.callback(
    Output("min", "children"),
    [Input("signal", "value"), Input('day', 'date')])
def update_min(signal, day):
    data = get_data(signal, day)
    return round(np.min(data.iloc[:,2]),1)

# Selectors -> max
@app.callback(
    Output("max", "children"),
    [Input("signal", "value"), Input('day', 'date')])
def update_max(signal, day):
    data = get_data(signal, day)
    return round(np.max(data.iloc[:,2]),1)

# Selectors -> Q1
@app.callback(
    Output("Q1", "children"),
    [Input("signal", "value"), Input('day', 'date')])
def update_q1(signal, day):
    data = get_data(signal, day)
    return round(np.quantile(data.iloc[:,2], .25),1)

# Selectors -> Q3
@app.callback(
    Output("Q3", "children"),
    [Input("signal", "value"), Input('day', 'date')])
def update_q3(signal, day):
    data = get_data(signal, day)
    return round(np.quantile(data.iloc[:,2], .75),1)

# Selectors -> Values null
@app.callback(
    Output("vall_null", "children"),
    [Input("signal", "value"), Input('day', 'date')])
def update_vall_null(signal, day):
    data = get_data(signal, day)
    return sum(data.iloc[:,2].isnull())

# Main table -> data details
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(signal, day):
    
    data = get_data(signal, day)
    
    data_statistics_group = data.groupby("groupings").count()
    
    return dcc.send_data_frame(data_statistics_group.to_csv, r"data_statistics_{}.csv".format(signal), index=False)

# Main
if __name__ == "__main__":
    app.run_server(debug=True, 
                   use_reloader=False)