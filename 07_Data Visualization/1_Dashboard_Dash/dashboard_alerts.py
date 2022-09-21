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
import pandas as pd

#import plotly.io as pio
#pio.renderers.default='browser'

#DataBases Master
df_dash = pd.read_csv("data/df_dash.csv")
#formato de datos para desplegar mejor la tabla en front end
df_ideal = pd.read_csv("data/df_ideal.csv")

df_ideal['pais'] = 'Argentina'
df_ideal = df_ideal.loc[:,['pais','day', 'Avg', 'Stddev', 'Min', 'Max', 'Q1', 'Q2', 'Q3',
                           'Count', 'Cantidad_CU', 'signal', 'Grado', 'Velocidad', 'Ancho', 'iqr',
                           'outlierDown_y', 'outlierUp_y', 'pct_val_no_zero',
                           'pct_val_zero', 'pct_val_null', 'validacion']]

input_country = 'Argentina'
list_signal = ["hsa12_loopout_eslsprtrdactpst_C1075052642",
               "hsa12_loopout_esrsprtrdactpst_C1075052644",
               "hsa12_loopout_eslsprtrdactrod_C1075052643",
               "hsa12_loopout_esrsprtrdactrod_C1075052645"]


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
            dcc.Dropdown(df_dash["signal"].unique(),
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
def filter_dataframe(df_dash, input_country, list_signal):
    dff = df_dash[ (df_dash["pais"].isin([input_country])) 
            & (df_dash.stack().str.contains('|'.join(list_signal)).any(level=0)) ]
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

    dff = filter_dataframe(df_dash, input_country, list_signal)
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
    dff = filter_dataframe(df_dash, input_country, list_signal)
    return dff[dff["indicador"] == 'estable'].shape[0]

# Main graph -> graph bar
@app.callback(
    Output(component_id = 'fig',
           component_property = 'figure'),
    [
     Input("input_country", "value"),
     Input("list_signal", "value")
    ])
def update_fig_0(input_country, list_signal):

    dff = filter_dataframe(df_dash, input_country, list_signal)
    
    fig = go.Figure()

    tmp = dff.groupby(["pais","signal","indicador"], as_index = False).count().iloc[:,:4]
    #tmp["x"] = tmp['pais'] + "|" + tmp['linea'].astype(str) + "|" + tmp['segmento'].astype(str)
    #tmp = tmp.iloc[:,[5,3,4]]
    #tmp.columns = ["x","status_alerta","y"]
    
    fig = px.bar(tmp,
                 x="signal",
                 y="Unnamed: 0",
                 color="indicador",
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

    dff = filter_dataframe(df_dash, input_country,list_signal)    

    fig = go.Figure()
        
    fig = px.scatter(
        dff,
        x="pct_val_no_zero",
        y="estable", 
        color="indicador",
        color_discrete_sequence=["red", "green", "yellow"],
        size='Cantidad_CU', 
        hover_data=['key_group'],
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
    
    dff = filter_dataframe(df_ideal, input_country, list_signal)
    
    trace_0 = go.Table(
        header=dict(values=list(dff.columns),
                    fill_color='paleturquoise',
                    align='center'),
                
        cells=dict(values=[dff.pais, dff.day,dff.Avg, dff.Stddev, dff.Min, dff.Max, dff.Q1, dff.Q2, dff.Q3,
                           dff.Count, dff.Cantidad_CU, dff.signal, dff.Grado, dff.Velocidad, dff.Ancho, dff.iqr,
                           dff.outlierDown_y, dff.outlierUp_y, dff.pct_val_no_zero,
                           dff.pct_val_zero, dff.pct_val_null, dff.validacion],
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
