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
df_comparative_sample = pd.read_csv("data/df_comparative_sample.csv")

df_dash = pd.read_csv("data/df_dash.csv")

df_ideal = pd.read_csv("data/df_ideal.csv")

#Filtros ddebbug
input_country = 'Argentina'
list_signal = ["hsa12_loopout_eslsprtrdactpst_C1075052642",
               "hsa12_loopout_esrsprtrdactpst_C1075052644",
               "hsa12_loopout_eslsprtrdactrod_C1075052643",
               "hsa12_loopout_esrsprtrdactrod_C1075052645"]

app = dash.Dash( __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}] )
app.title = "Monitorea Predictivo"
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
                
                html.Div([html.H6(id="n_signal"),
                          html.P("No. de señales")],
                         className="mini_container"),
                
                html.Div([html.H6(id="n_groups"),
                          html.P("Grupos")],
                         className="mini_container"),
                
                html.Div([html.H6(id="n_groups_found"),
                          html.P("Grupos encontrados")],
                         className="mini_container"),
                
                html.Div([html.H6(id="groups_no_found"),
                          html.P("Grupos no encontrados")],
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
    dff = df_dash[ (df_dash["country"].isin([input_country])) 
            & (df_dash.stack().str.contains('|'.join(list_signal)).any(level=0)) ]
    return dff

# Create callbacks

# Selectors -> n_signals text
@app.callback(
    Output("n_signal", "children"),
    [Input("input_country", "value"),
     Input("list_signal", "value")])
def update_n_signal(input_country, list_signal):

    dff = filter_dataframe(df_dash, input_country, list_signal)
    return len(dff["signal"].unique())

# Selectors -> n_groups text
@app.callback(
    Output("n_groups", "children"),
    [Input("input_country", "value"),
     Input("list_signal", "value")])
def update_n_groups(input_country, list_signal):
    dff = filter_dataframe(df_dash, input_country, list_signal)
    return len(dff["key_group"].unique())

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

    tmp = dff.groupby(["country","signal","indicator"], as_index = False).count().iloc[:,:4]
    tmp.columns = ["country","x","indicator","y"]
    
    fig = px.bar(tmp,
                 x="x",
                 y="y",
                 color="indicator",
                 color_discrete_sequence=["green", "red", "yellow"],
                 title="Conteo de los status de una señal")
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
        x="pct_val_no_zeros",
        y="within_range", 
        color="indicator",
        color_discrete_sequence=["green", "red", "yellow"],
        size='Cantidad_CU_may22', 
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
                
        cells=dict(values=[dff.country,dff.day, dff.signal, dff.Grado_may22,
                           dff.Velocidad_may22, dff.Ancho_may22, dff.key_group,
                           dff.Count_may22, dff.Avg_may22, dff.Stddev_may22, 
                           dff.Min_may22, dff.Max_may22, dff.Q1_may22,
                           dff.Q2_may22, dff.Q3_may22, dff.iqr_may22, dff.outlierDown_may22,
                           dff.outlierUp_may22, dff.Cantidad_CU_may22, dff.pct_val_no_zeros,
                           dff.pct_val_equal_zero, dff.pct_val_null, dff.sum_validation_completeness,
                           dff.within_range, dff.out_lower_range, dff.out_upper_range,
                           dff.sum_validation_ouliter_ranges, dff.indicator],
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
