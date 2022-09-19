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

#Data Processing
import dask.dataframe as dd
import pandas as pd

#import plotly.io as pio
#pio.renderers.default='browser'

#utils
from utils import values 
from utils import transformations

#Load data Azure
date = '20220902'

ddf = dd.read_parquet(f'abfs://arg-landing-iba-sns-ccd2@prodllanding.blob.core.windows.net/date={date}',
                      storage_options = {"account_name": values.config_values['Signals']['account_name'],
                                         "sas_token": values.config_values['Signals']['sas_token']},
                      blocksize = None,
                      columns = values.config_values['Signals']['columns_file'])

ddf_may = dd.read_csv('abfs://mtto-predictivo-input-arg@prodltransient.blob.core.windows.net/202205_ccd2_iba_ideal.csv',
                       storage_options = {"account_name": values.config_values['May22']['account_name'],
                                         "sas_token": values.config_values['May22']['sas_token']},
                       blocksize = None).compute()

#Transformations
ddf = transformations.format_groups(ddf).compute()

#Muestra ideal Mayo 2022

#status_completitud

#status_cu

#status_outlier

#status_alerta

#DataBases Master
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
                dcc.Graph(id = 'fig_1'),

                ],
                id="countGraphContainer",
                className="pretty_container")],
            id="right-column",
            className="eight columns")
        ],
        className="row flex-display"
        ),
        
        dbc.Row(dbc.Col(html.H3(children="Detalle de la información : "))),
        dcc.Graph(id = 'table_1'),
        
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

# Main table -> data details
@app.callback(
    Output("table_1", "figure"),
    [
     Input('input_country', 'value'),
     Input("list_signal", "value")
    ])
def table_details(input_country, list_signal):
    
    dff = filter_dataframe(df, input_country,list_signal)
    
    trace_0 = go.Table(
        header=dict(values=list(dff.columns),
                    fill_color='paleturquoise',
                    align='center'),
                
        cells=dict(values=[dff.pais, dff.dia, dff.linea, dff.segmento, dff.grado_acero, dff.velocidad_linea,
                           dff.ancho_slab, dff.signal, dff.status_completitud, dff.status_outlier,
                           dff.status_cu, dff.status_alerta],
                   fill_color='lavender',
                   align='center'))

    layout_0 = go.Layout(legend = {"x":.9,"y":.5},  margin=dict(l=20, r=20, t=20, b=20),
                         height = 4400,
                         showlegend = False,
                         template = 'ggplot2',
                         )

    fig_1 = go.Figure(data = [trace_0], layout = layout_0)

    return fig_1

# Main
if __name__ == "__main__":
    app.run_server(debug=True, 
                   use_reloader=False)
