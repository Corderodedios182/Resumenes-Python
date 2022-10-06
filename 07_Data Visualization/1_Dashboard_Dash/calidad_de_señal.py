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

#import plotly.io as pio
#pio.renderers.default='browser'

#Data Processing
import pandas as pd
from datetime import date
import datetime
from datetime import datetime, timedelta

#DataBases Master
ddf_signal = dd.read_csv("data/ddf_signal/*.csv").compute()
ddf_signal['Time'] = pd.to_datetime(ddf_signal['Time'])

def get_data(señal, dias, dia):
    
    inicio = datetime.strptime(str(dia), '%Y-%m-%d') - timedelta(days= int(dias))    
    fin =    datetime.strptime(str(dia), '%Y-%m-%d') + timedelta(days= int(dias))
    
    return ddf_signal[(ddf_signal["Time"] >= inicio) & (ddf_signal["Time"] <= fin)].loc[:,["Time","groupings",señal]]

#Filtros ddebbug
input_country = 'Argentina'
list_signal = ["hsa12_group_hsarefgaubs_C1075052604", "hsa12_group_hsaactgauts_C1075052605","hsa12_loopout_dslsprtrdactpst_C1075052646", "hsa12_loopout_dslsactfrc_C1075052640"]

start_date = '2022-10-01'
end_date = '2022-10-02'

app = dash.Dash( __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}] )
app.title = "Monitorea Predictivo"
server = app.server

####################
# Create app layout#
#################a###
app.layout = html.Div([
    #Header
    html.Div(className="study-browser-banner row",
             children=[html.H2(className="h2-title", children="Alertas de Señales Desviadas "),
                       html.Div(className="div-logo",
                                children=html.Img(className="logo", src=app.get_asset_url("Ternium.png"))),
                       html.H2(className="h2-title-mobile", children="Alertas de Señales Desviadas ")
                       ]),
    #DropdownMenu
    html.Div([
        html.Br(),
        html.P("País : ", className="control_label"),
        dcc.RadioItems(
            id="input_country",
            options=[{"label": "ARG ", "value": "Argentina"},
                     {"label": "BRA ", "value": "Brasil"},
                     {"label": "MEX ", "value": "México"}],
            value="Argentina",
            labelStyle={"display": "inline-block"},
            className="dcc_control"),
        html.Br(),
        html.P("Listado de señales :", className="control_label"),
        dcc.Dropdown(ddf_signal.columns[1:-1],
                     id ='signal',
                     multi=True),
        html.Br(),
        html.P("Rango de fechas :", className="control_label"),
        dcc.DatePickerRange(
            id='day',
            min_date_allowed = datetime.today() + timedelta(days =-30),
            max_date_allowed = datetime.today(),
            start_date_placeholder_text="Start Period",
            end_date_placeholder_text="End Period") 
        ]),
    html.Br(),
    
    #tabla por días señal | día | estable | media | revisión
    html.Div([
        html.P("Clasificación de las señales :", className="control_label"),
        dcc.Graph(id = 'table_1'),
        html.P("Señales a revisar :", className="control_label"),
        dcc.Graph(id = 'table_2'),
        html.Br(),
        dcc.Graph(id = 'fig'),
        html.Br(),
        dcc.Graph(id = 'fig_1'),
        html.P("Detalle de la información :", className="control_label"),
        html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv")],
        id="countGraphContainer",
        className="pretty_container")
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"}
    )

###################
# Helper functions#
###################

# Main
if __name__ == "__main__":
    app.run_server(debug=True, 
                   use_reloader=False)
