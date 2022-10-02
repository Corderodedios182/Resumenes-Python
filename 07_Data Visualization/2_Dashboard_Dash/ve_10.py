# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 10:54:36 2022
@author: cflorelu
"""
#from operator import is_not
import dash
import dash_html_components as html
from dash import Dash, dcc, html, ctx, dash, dash_table
from dash.dependencies import Input, Output, State
from dash_table import DataTable

from dash import Dash, dcc, html, ctx, dash, dash_table
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objs as go
from scipy import stats
from dash import dash_table

from datetime import date, timedelta, datetime
import dash_bootstrap_components as dbc
import dash_daq as daq

import numpy as np

import dask
import dask.dataframe as dd
import pandas as pd
import numpy as np

import os.path

app = Dash(__name__)

if os.path.exists('data.csv') == True:
    os.remove("data.csv")

group_colors = {"control": "light blue", "reference": "red"}

#################
#Valores Filtros#
#################
signals = ["Time",
        "s4_an2l_ramactwidthboc_C1611", #ancho plataforma
        "s4_hmo_pmac_fmplc_m5043_an2l_hmo_castspeed_C0470", #velodicdad línea
        "grade_number_C1074659440", #grado_acero
        "s4_drv_net_a_ea_seg12_torque_reff_C1074856029", #señales de línea 4 y segmento 12
        "s4_drv_net_a_ea_seg12_torque_ref_C1074856020",
        "hsa12_loopout_eslsprtrdactpst_C1075052642",
        'hsa12_group_hsarefgauts_C1075052603']

#Transformaciones#
##################
@dask.delayed
def format_groups(df):
    """Formato a las señales extraidas.
    Agrupa por segundo para disminuir los datos de milisegundos a segundos.
    Crea etiquetas y grupos de ancho, velocidad y grado de acero.
    """
    df['Time'] = df["Time"].dt.year.astype(str)  +"-" + \
                df["Time"].dt.month.astype(str) +"-" + \
                df["Time"].dt.day.astype(str)   +" " + \
                df["Time"].dt.hour.astype(str)  +":" + \
                df["Time"].dt.minute.astype(str)+":" + \
                df["Time"].dt.second.astype(str)
    df['Time'] = pd.to_datetime(df['Time'])
    df = df.groupby(["Time"]).mean().reset_index()
    return df


def get_data(señal, dias, dia):

    #Valores Filtros#
    #################
    signals = ["Time",
            señal]
    
    #Valores Azure#
    ###############
    config_values = {'Signals': {
                        'account_name': 'prodllanding',
                        'sas_token': 'sp=rl&st=2022-04-05T18:14:27Z&se=2023-01-01T03:14:27Z&sv=2020-08-04&sr=c&sig=%2Fqe%2F4HbbTL6Tvx2oYNkF2tV7Qjjdj%2BsO2fDdldVinUU%3D', 
                        'source': 'abfs://arg-landing-iba-sns-ccd2@prodllanding.blob.core.windows.net/date={date_}',
                        'columns_file': signals,
                        'columns_order': signals,
                        'columns_to_date': ['Time'],
                        'skip_rows': 0,
                        'output_ddf': 'ddf'
                        }
                    }
    ################

    #CREACION DE day_files
    inicio = datetime.strptime(str(dia), '%Y-%m-%d') - timedelta(days= int(dias))    
    fin =    datetime.strptime(str(dia), '%Y-%m-%d') + timedelta(days= int(dias))
    print(fin)

    lista_dias = []
    i = 0
    while i < 10:

        dias_seleccionados = inicio + timedelta(days= (i))
        if dias_seleccionados == fin:
                lista_dias.append(dias_seleccionados.strftime('%Y%m%d'))
                break
        else:
            lista_dias.append(dias_seleccionados.strftime('%Y%m%d'))
        
        i=i+1

    day_files=lista_dias
    day_files
    print(day_files)
    
    #EXTRACCION DE DATOS
    df_list=[]
    for i in day_files:
        print(i)
        ddf_signal = dd.read_parquet(f'abfs://arg-landing-iba-sns-ccd2@prodllanding.blob.core.windows.net/date={i}',
                        storage_options = {"account_name": config_values['Signals']['account_name'],
                                            "sas_token": config_values['Signals']['sas_token']},
                        blocksize = None,
                        columns = config_values['Signals']['columns_file'])
        df_list.append(format_groups(ddf_signal).compute())
    
    #CREACION DE PANDAS DATAFRAME
    
    df_final = pd.DataFrame()

    lista_time = []
    lista_datos = []
    for i in range(len(df_list)):
        lista_time = lista_time + df_list[i]['Time'].to_list()
        lista_datos = lista_datos + df_list[i][signals[1]].to_list()
        

    df_final['Time'] = lista_time
    df_final[señal] = lista_datos
    
    return df_final.drop_duplicates()



#===========================>Componenctes DCC
HEADER = html.H5('Calidad de señal')

SEÑAL = dcc.Dropdown([i for i in signals if i != 'Time'],id="señal")

TABS =  dcc.Tabs(id="tipo_grafico", value='tab-1-example-graph', children=[
        dcc.Tab(label='Histograma', value='histograma'),
        dcc.Tab(label='Señal en el tiempo', value='señal_tiempo'),
        ])

TABLA = dash_table.DataTable(id='table',
                            data=[])

DIA = dcc.DatePickerSingle(
            id='fecha',
            min_date_allowed=datetime(2022, 1, 1),
            max_date_allowed=datetime(2022, 12, 2))


TEXTO = dcc.Textarea(
        id='textarea-example-output',
        value='Textarea content initialized\nwith multiple lines of text',
        style={'width': '100%', 'height': 300},
    )
BOTON=html.Button('Filtrar', id='textarea-state-example-button', n_clicks=0),
TEXTO=html.Div(id='textarea-state-example-output', style={'whiteSpace': 'pre-line'})
GRAFICO_GENERAL=dcc.Graph(id='grafico',
                        figure={'data':[
                        {'x':[1,2],'y':[3,1]}
                        ]}              
                    )
GRAFICO_UN_DIA = dcc.Graph(id='grafico_un_dia',
                        figure={'data':[
                        {'x':[1,2],'y':[3,1]}
                        ]}              
                    )

SLIDER = dcc.Slider(0, 2,
    step=None,
    marks={
        1: '1',
        2: '2',

    },
    value=1000,
    id='slider'
)

    
columnas = [
    {"id": 0, "name": "Métricas"},
    {"id": 1, "name": "Valores"},
    ]    


#=============================>LAYOUT
# App Layout
app.layout = html.Div(
    children=[
        # Error Message
        html.Div(id="error-message"),
        # Top Banner
        html.Div(
            className="study-browser-banner row",
            children=[
                html.H2(className="h2-title", children="CALIDAD DE SEÑAL"),
                html.Div(
                    className="div-logo",
                    children=html.Img(
                        className="logo", src=app.get_asset_url("Ternium.png")
                    ),
                ),
                html.H2(className="h2-title-mobile", children="CALIDAD DE SEÑAL"),
            ],
        ),
        # Body of the App
        html.Div(
            className="row app-body",
            children=[
                # User Controls
                html.Div(
                    className="four columns card",
                    children=[
                        html.Div(
                            className="bg-white user-control",
                            children=[
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        html.H6("SELECCIONA SEÑAL"),
                                        dcc.Dropdown([i for i in signals if i != 'Time'],id="señal"),
                                    ],
                                ),
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        html.H6("ABALIZAR UN DÍA"),
                                        DIA
                                    ]
                                ),
                                
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        html.H6(" "),
                                            html.Button('Buscar Señal', id='boton', n_clicks=0)
                                    ]
                                ),
                                html.Div(
                                    className="padding-top-center",
                                    children=[
                                        html.H6(' '),
                                        html.H6(" "),
                                        dcc.Loading(
                                            id="loading-1",
                                            type="default",
                                            children=html.Div(id="loading")
                                        ),
                                        html.H6(' ')
                                    ]
                                ),
                                
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                            html.Br(' '),
                                            html.H6("SELECCIONA TIPO DE GRAFICO"),
                                            dcc.Tabs(id="tipo_grafico", children=[
                                            dcc.Tab(label='Histograma', value='histograma'),
                                            dcc.Tab(label='Señal en el tiempo', value='señal_tiempo'),
                                            ]
                                        ),
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
                
                # Graph
                html.Div(
                    className="eight columns card-left",
                    children=[
                        html.Div(
                            className="bg-white",
                            children=[
                                html.H5(id='descripcion'),
                                dcc.Graph(id="plot",
                                        figure={'data':[
                                            {'x':[1,2],'y':[3,1]}
                                            ]}),
                            ],
                        ),
                        html.Div(
                            className="eight columns card-right",
                            children=[
                                html.Div(
                                className="bg-white-3",
                                children=[
                                            html.H5("MÉTRICAS"),
                                            dash_table.DataTable(
                                            id='table',
                                            data=[]
                                            )
                                    ],
                                ),               
                            ],
                        ),
                        
                        html.Div(
                            className="four columns card-right",
                            children=[
                                html.Div(
                                    className="bg-white-2",
                                    children=[
                                                    html.H5("VALORES NULOS"),
                                                    daq.Gauge(
                                                        showCurrentValue=True,
                                                        min=0,
                                                        id='valores_nulos',
                                            )
                                    ],
                                ),               
                            ],
                        ),
                    ],
                ),  
            ],
        ),
    ]
)


#=============================> callbacks
@app.callback(
    
    [Output('descripcion','children'),
    Output("loading", "children"),
    Output("table", "data"),
    Output('table', 'columns')],
    
    [Input('fecha', 'date'),
    Input("señal", "value"),
    Input("loading", "value"),
    Input('boton','n_clicks')]
    
)
def update_descripcion(fecha,señal,value,boton):
    if 'boton' == ctx.triggered_id:
        
        if os.path.exists('data.csv') == True:
            os.remove("data.csv")
    
        data=get_data(señal,1,fecha)
        
        print(data[señal].unique())
        
        data.to_csv('data.csv',index = False)

        inicio = datetime.strptime(str(fecha), '%Y-%m-%d')\
                    - timedelta(days= int(1))
                        
        fin = datetime.strptime(str(fecha), '%Y-%m-%d') \
                    + timedelta(days= int(1))

        info = data[[data.columns[1]]].describe().reset_index()
        info.columns=['Métricas','Valores']
                
        return 'Rango de dias seleccionados ' + str(inicio.date()) +\
                ' - ' + str(fin.date()), value, info.values[0:9],   [
                                                                    {"id": 0, "name": "Métricas"},
                                                                    {"id": 1, "name": señal},
                                                                    ] 


@app.callback(
    Output("plot", "figure"),
    [Input("señal", "value"), 
    Input("tipo_grafico", "value"),
    Input('fecha', 'date')]
)
def update_grafico(señal, tipo_grafico, fecha):
    print(tipo_grafico, type(fecha))
    data = pd.read_csv('data.csv')  
    if tipo_grafico == 'histograma':
                #info = data[(data['Time'] == señal_inicio)][[value]]
                #info = data[data.Time.dt.strftime('%Y-%m-%d') == fecha][[señal]]
                #info = data[[señal]]
            bar_graph = px.histogram(data_frame = data[[señal]], title=señal, x = señal)
                
                
            return bar_graph
            
    elif tipo_grafico == 'señal_tiempo':
                
                #info = pd.DataFrame()
                #info['tiempo'] = data.index
                #info['señal'] = data[data.Time.dt.strftime('%Y-%m-%d') == fecha][[señal]]
                
            bar_graph=px.line(data_frame = data, x = [d for d in data['Time']], y = señal, title=señal) 
                
            return bar_graph
    
    else:
    
        return {}



@app.callback(
    [Output("valores_nulos", "value"),
    Output('valores_nulos', 'max')],
    [Input("señal", "value"), Input("tipo_grafico", "value")]
)
def update_valores_nulos(señal,tipo_grafico):

    if 'tipo_grafico' == ctx.triggered_id: 
        print('jksfnkjefnkwnfksaj')
        df = pd.read_csv('data.csv')
        total_valores = df.shape[0]
        valores_nulos = df[señal].isna().sum()
            
        print(valores_nulos, total_valores)
                    
        return valores_nulos, total_valores
    else: 
        return 0,10




if __name__ == "__main__":
    app.run_server(port=8053)