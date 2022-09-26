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
                
                dcc.Graph(id = 'table_1')
                
                ],
                id="info-container",
                className="row container-display"
                    ),
            
            #Views : graphs and tables.
            html.Div([
                
                dcc.Graph(id = 'fig'),
                dcc.Graph(id = 'fig_1'),
                html.P("Detalle de la información :", className="control_label"),
                html.Button("Download CSV", id="btn_csv"),
                dcc.Download(id="download-dataframe-csv")

                ],
                id="countGraphContainer",
                className="pretty_container")],
            id="right-column",
            className="eight columns")
        ],
        className="row flex-display"
        ),
        
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

@app.callback(
    Output("table_1", "figure"),
    [
     Input('input_country', 'value'),
     Input("list_signal", "value")
    ])
def table_details(input_country, list_signal):

    dff = df_comparative_sample

    trace_0 = go.Table(
        header=dict(values=list(dff.columns),
                    fill_color='paleturquoise',
                    align='center'),

        cells=dict(values=[dff.feature,
                           dff.number],
                   fill_color='lavender',
                   align='center'))

    layout_0 = go.Layout(legend = {"x":.9,"y":.5},  margin=dict(l=20, r=20, t=20, b=20),
                         height = 200,
                         showlegend = False,
                         template = 'ggplot2',
                         )

    fig_1 = go.Figure(data = [trace_0], layout = layout_0)

    return fig_1

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
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df_ideal.to_csv, "información_detalle.csv")

# Main
if __name__ == "__main__":
    app.run_server(debug=True, 
                   use_reloader=False)
