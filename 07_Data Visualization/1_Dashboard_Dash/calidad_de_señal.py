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
from datetime import date
import datetime
from datetime import datetime, timedelta
import dask.dataframe as dd

#DataBases Master
ddf_signal = dd.read_csv("data/ddf_signal/*.csv").compute()
ddf_signal['Time'] = pd.to_datetime(ddf_signal['Time'])

def get_data(signal, day, days = 1):
    
    inicio = datetime.strptime(str(day), '%Y-%m-%d') - timedelta(days= int(days))    
    fin =    datetime.strptime(str(day), '%Y-%m-%d') + timedelta(days= int(days))
    
    return ddf_signal[(ddf_signal["Time"] >= inicio) & (ddf_signal["Time"] <= fin)].loc[:,["Time","groupings",signal]]

#Filtros ddebbug
input_country = 'Argentina'
signal = "hsa12_group_hsarefgaubs_C1075052604"

day = '2022-10-02'

app = dash.Dash( __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}] )
app.title = "Calidad de la señal"
server = app.server

####################
# Create app layout#
#################a###
app.layout = html.Div(
    children=[
        
        # Error Message
        html.Div(id="error-message"),
        
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
                         children=[html.Div(children=[html.Div(children=[html.H6("SELECCIONA SEÑAL"),
                                                                         dcc.Dropdown(ddf_signal.columns[1:-1],
                                                                                      id = "signal")]),

                                                      html.Div(children=[html.H6("ABALIZAR UN DÍA"),
                                                                         dcc.DatePickerSingle(
                                                                                     id ='day',
                                                                                     min_date_allowed = datetime.today() + timedelta(days =-30),
                                                                                     max_date_allowed = datetime.today() ) ]),

                                                      html.Div(children=[html.H6(" "),
                                                                         html.Button('Buscar Señal', id='boton', n_clicks=0)]),

                                                      html.Div(children=[html.H6(' '),
                                                                         dcc.Loading(id="loading-1", type="default", children=html.Div(id="loading")),
                                                                         html.H6(' ')]),
                                                      
                                                      html.Div(children=[html.Br(' '),
                                                                         html.H6("SELECCIONA TIPO DE GRAFICO"),
                                                                         dcc.Tabs(id="type_graph", children=[
                                                                         dcc.Tab(label='Histograma', value='histograma'),
                                                                         dcc.Tab(label='Señal en el tiempo', value='señal_tiempo'),
                                                                         dcc.Tab(label='Señal en el tiempo por grupos', value='señal_tiempo_grupos')])])
                         ])])]),
                    # Graph
                    html.Div([
                        
                        html.Div(className="bg-white",
                                 children=[html.H5(id='descripcion'),
                                           dcc.Graph(id="plot",
                                                     figure={'data':[{'x':[1,2],'y':[3,1]}]} ) ] ),
                        html.Div(className="eight columns card-right",
                                 children=[html.Div(className="bg-white-3",
                                                    children=[html.H5("MÉTRICAS"),
                                                              dash_table.DataTable(id='table',
                                                                                   data=[] ) ] ) ]
                            )],
                        id="countGraphContainer",
                        className="pretty_container")
                    ])

#=============================> callbacks
@app.callback(
    Output("plot", "figure"),
    [Input("signal", "value"), 
     Input("type_graph", "value"),
     Input('day', 'date')]
)
def update_grafico(signal, type_graph, day):
    
    data = get_data(signal, day)
    data.columns = ["Time", "groupings", "value"]
    
    if type_graph == 'histograma':
        
        bar_graph = px.histogram(data_frame = data[[signal]], title = signal, x = signal)
        
        return bar_graph
            
    elif type_graph == 'señal_tiempo':
        
        bar_graph=px.line(data_frame = data, x = [d for d in data['Time']], y = signal, title = signal) 
                
        return bar_graph
        
    elif type_graph == 'señal_tiempo_grupos':
        
        bar_graph = px.scatter(
            data,
            x = "Time",
            y = "value", 
            color = "groupings",
            width = 1600,
            height = 700,
            title = r"Grupos generados por señal : {}".format(signal))

        return bar_graph
    
    else:
    
        return {}

# Main
if __name__ == "__main__":
    app.run_server(debug=True, 
                   use_reloader=False)