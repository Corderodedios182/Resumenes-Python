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
import dash_table

import dash_html_components as html
import dash_bootstrap_components as dbc
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

from utils import values
from utils import extract_month_azure

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
                                                                         dcc.Dropdown(options = values.signals[1:],
                                                                                      id = "signal",
                                                                                      value = values.signals[1:][0]),
                                                                                      ]),

                                                      html.Div(children=[html.H6("Selecciona un día : "),
                                                                         dcc.DatePickerSingle(
                                                                                     id ='day_gregorate',
                                                                                     date = datetime.today() - timedelta(days= int(1)),
                                                                                     
                                                                                     min_date_allowed = datetime.today() + timedelta(days =-30),
                                                                                     max_date_allowed = datetime.today() ) ]),
                                                      
                                                      html.Div(children=[html.H6("Selecciona un grado de acero : "),
                                                                                                      dcc.Dropdown(values.grados,
                                                                                                                   id = "grado_acero",
                                                                                                                   value = values.grados,
                                                                                                                   multi=True)]),

                                                      html.Div(children=[html.H6(" "),
                                                                         html.Button('Consultar datos de Señal : ', id='boton', n_clicks=0)]),

                                                      html.Div(children=[html.H6(' '),
                                                                         dcc.Loading(id="loading-1", type="default", children=html.Div(id="loading")),
                                                                         html.H6(' ')]),
                                                      
                                                      html.Div(children = [html.Br(' '),
                                                                           html.H6('Estadísticas descriptivas de la señal.'),
                                                                           dash_table.DataTable(
                                                                                   id="table_signal_statistics",
                                                                                   style_as_list_view=True,
                                                                                   editable=False,
                                                                                   style_table={"overflowY": "scroll",
                                                                                                "width": "100%",
                                                                                                "minWidth": "100%",
                                                                                                },
                                                                                     style_header={"backgroundColor": "#d96210", "fontWeight": "bold"},
                                                                                     style_cell={"textAlign": "center", "padding": "10px"},
                                                                                     )]),
                                                      
                                                      html.Div(children=[html.Br(' '),
                                                                         html.H6("Selecciona un tipo de gráfico : "),
                                                                         dcc.Tabs(id="type_graph", value = 'histograma',
                                                                                  children=[
                                                                                      dcc.Tab(label='Histograma', value='histograma'),
                                                                                      dcc.Tab(label='Señal en el tiempo', value='señal_tiempo'),
                                                                                      dcc.Tab(label='Señal en el tiempo por grupos', value='señal_tiempo_grupos')]
                                                                                  )]),
                                                      
                         ])])]),
                    # Graph
                    html.Div([
                        dcc.Graph(id="plot"),
                        html.P("Detalle de la información :", className="control_label"),
                        html.Button("Download CSV", id="btn_csv_fails"),
                        dcc.Download(id="download-dataframe-csv")
                        ],
                        id="countGraphContainer",
                        className="pretty_container")
                    ])

###################
# Helper functions#
###################
#Filtros ddebbug
signal = "hsa12_loopout_esrsprtrdactrod_C1075052645"
day_gregorate = '2022-10-09'
days = 2
grado_acero = [7011]
def get_data(signal = "hsa12_loopout_esrsprtrdactrod_C1075052645",
             day_gregorate = '2022-10-09',
             days = 0,
             grado_acero = []):
    
    extract_month_azure.azure_data_extraction(day_gregorate = day_gregorate, days = days)

    ddf_signal = dd.read_csv(r"data/ddf_signal/ddf_signal_{}.csv".format(day_gregorate.replace("-",""))).compute()
    ddf_signal['Time'] = pd.to_datetime(ddf_signal['Time'])
    
    columns = ["Time","groupings","grado_acero",signal]
    
    if len(grado_acero) != 0:
        data =  ddf_signal[(ddf_signal["grado_acero"].isin(grado_acero))].loc[:,columns]
    else: 
        data = ddf_signal.loc[:,columns]
        
    data.columns = ["Time", "groupings", "grado_acero", "value"]
    
    return data

##################
#Create callbacks#
##################

@app.callback(
    Output("plot", "figure"),
    [Input("signal", "value"),
     Input("type_graph", "value"),
     Input('day_gregorate', 'date'),
     Input("grado_acero", "value")     ]
)
def update_grafico(signal,
                   type_graph,
                   day_gregorate,
                   grado_acero):
    """Muestra el tipo de gráfico a visualzar"""
    data = get_data(signal = signal,
                    day_gregorate = day_gregorate,
                    days = 0,
                    grado_acero = grado_acero)

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
        bar_line = px.scatter(data_frame = data,
                           x = data["Time"],
                           y = data["value"],
                           title = r"Serie de tiempo señal : {}".format(signal)) 
        return bar_line
    elif type_graph == 'señal_tiempo_grupos':
        scatter_graph = px.scatter(
            data,
            x = "Time",
            y = "value", 
            color = "groupings",
            title = r"Serie de tiempo grupos : Grado | Velocidad | Ancho : {}".format(signal))
        
        scatter_graph.update_traces(hovertemplate=None)
        scatter_graph.update_layout(hovermode="x")
        
        return scatter_graph
    else:
        return {}


# Selectors -> table_signal_statistics
@app.callback(
    [Output("table_signal_statistics", "data"),
     Output("table_signal_statistics", "columns")],
    [Input("signal", "value"),
     Input('day_gregorate', 'date'),
     Input('grado_acero', 'value')]
    )
def update_table_signal_statistics(signal,
                                   day_gregorate,
                                   grado_acero):
    
    data = get_data(signal = signal,
                    day_gregorate = day_gregorate,
                    grado_acero = grado_acero)
    
    signal_statistics = data["value"].describe().reset_index()
    signal_statistics = pd.pivot_table(signal_statistics, values = "value", columns = "index")
    signal_statistics["registros_nulos"] = sum(data.loc[:,"value"].isnull())
    signal_statistics = round(signal_statistics,1)

    return signal_statistics.to_dict('records'), [{"name": i, "id": i} for i in signal_statistics.columns]

# Main table -> data details
@app.callback(
    Output("download-dataframe-csv", "data"),
    [Input("btn_csv", "n_clicks"),
     Input("signal", "value"),
     Input('day_gregorate', 'date'),
     Input('grado_acero', 'value')],
     prevent_initial_call =True
    )
def func(n_clicks,
         signal,
         day_gregorate,
         grado_acero):
    
    if (n_clicks is None):
        data = get_data(signal = signal,
                        day_gregorate = day_gregorate,
                        grado_acero = grado_acero)
    
        data_statistics_group = data.groupby("groupings",as_index = False).agg(['min', 'max']).reset_index()
        
        return dcc.send_data_frame(data_statistics_group.to_csv, r"data_statistics_{}.csv".format(signal), index=False)
    else: None
        
# Main
if __name__ == "__main__":
    app.run_server(debug=True, 
                   use_reloader=False)