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

import plotly.io as pio
pio.renderers.default='browser'

#utils
from utils import values 
from utils import transformations

#Load data Azure
day_gregorate = '2022-09-02'
day_files = '20220902'

ddf_signal = dd.read_parquet(f'abfs://arg-landing-iba-sns-ccd2@prodllanding.blob.core.windows.net/date={day_files}',
                      storage_options = {"account_name": values.config_values['Signals']['account_name'],
                                         "sas_token": values.config_values['Signals']['sas_token']},
                      blocksize = None,
                      columns = values.config_values['Signals']['columns_file'])

ddf_may = dd.read_csv('abfs://mtto-predictivo-input-arg@prodltransient.blob.core.windows.net/202205_ccd2_iba_ideal.csv',
                       storage_options = {"account_name": values.config_values['May22']['account_name'],
                                         "sas_token": values.config_values['May22']['sas_token']},
                       blocksize = None).compute()

#Transformations
ddf_signal = transformations.format_groups(ddf_signal).compute()

#Status_completitud (Por toda la señal)
ddf_time = transformations.seconds_day(day_gregorate).compute()

ddf_complete = dd.merge(ddf_time,
                        ddf_signal.iloc[:,:-1],
                        on='Time',
                        how='left').compute()

ddf_zero = transformations.missing_groups(ddf_complete, value = 'zero').compute()
ddf_no_zero = transformations.missing_groups(ddf_complete, value = 'no_zero').compute()
ddf_null = transformations.missing_groups(ddf_complete, value = 'null').compute()

ddf_missing_groups = pd.merge(ddf_no_zero, ddf_zero, on = 'signals', how = 'outer')
ddf_missing_groups = pd.merge(ddf_missing_groups, ddf_null, on = "signals", how = 'outer')
ddf_missing_groups = ddf_missing_groups.fillna(0)

ddf_missing_groups["validacion"] =  ddf_missing_groups["pct_val_zero"] + ddf_missing_groups["pct_val_no_zero"] + ddf_missing_groups["pct_val_null"]
ddf_missing_groups = ddf_missing_groups.loc[:,['day_x','signals','pct_val_no_zero','pct_val_zero','pct_val_null', 'validacion']]
ddf_missing_groups = ddf_missing_groups.sort_values("pct_val_zero", ascending = False)
ddf_missing_groups["day_x"] = day_gregorate

#Muestra ideal Mayo 2022
ddf_may["Grado"] = ddf_may["Grado"].astype(int)
ddf_may["Velocidad"] = ddf_may["Velocidad"].apply(lambda x: round(x, 1))

ddf_may["key_group"] = ddf_may["signal"].astype(str) + " | " + \
                       ddf_may["Grado"].astype(str) + " | " + \
                       ddf_may["Velocidad"].astype(str) + " | " + \
                       ddf_may["Ancho"].astype(str)

ddf_may["iqr"] = ddf_may["Q3"] - ddf_may["Q1"]
ddf_may["outlierDown"] = ddf_may["Q1"] - (1.5 * ddf_may["iqr"])
ddf_may["outlierUp"] = ddf_may["Q3"] + (1.5 * ddf_may["iqr"])

ddf_may_tmp = ddf_may[ddf_may["signal"].str.contains("hsa12_loopout_dslsprtrdactpst_C1075052646")]

#status_outlier y status_cu
ddf_complete = dd.merge(ddf_time,
                        ddf_signal,
                        on='Time',
                        how='left').compute()

ddf_complete = pd.melt(ddf_complete,
                       id_vars = ["Time","second_day",'groupings'],
                       value_vars = ddf_complete.columns[1:])

ddf_complete["groupings"] = ddf_complete["groupings"].fillna("no_group")
ddf_complete["value"] = ddf_complete["value"].fillna(.99)

ddf_complete["key_group"] = ddf_complete["variable"] + " | " + \
                            ddf_complete["groupings"].astype(str)

ddf_complete_tmp = ddf_complete[ddf_complete["variable"] == 'hsa12_loopout_dslsprtrdactpst_C1075052646']

#¿Cuantos grupos se encuentran en las muestras ideales de mayo 2022?
groups_may =  ddf_may_tmp["key_group"].unique()
groups_complete_tmp = ddf_complete_tmp["key_group"].unique()

encontradas = [item in groups_complete_tmp for item in groups_may]
print("No se encontraron ", groups_complete_tmp.shape[0] - sum(encontradas) , " grupos de muestra para está señal")

ddf_complete_tmp = ddf_complete_tmp.merge(ddf_may, on='key_group', how = 'left')

encontrados_may = ddf_complete_tmp[~ddf_complete_tmp["Avg"].isnull()]["key_group"].unique()
no_encontrados_may = ddf_complete_tmp[ddf_complete_tmp["Avg"].isnull()]["key_group"].unique()

ddf_complete_tmp = ddf_complete_tmp[~ddf_complete_tmp["Avg"].isnull()]

ddf_complete_tmp["status_outlier"] = 'estable'

ddf_complete_tmp.loc[ddf_complete_tmp["value"] >= ddf_complete_tmp["outlierUp"], "status_outlier"] = 'outlierUp'
ddf_complete_tmp.loc[ddf_complete_tmp["value"] <= ddf_complete_tmp["outlierDown"],"status_outlier"] = 'outlierDown'

df_outlier = ddf_complete_tmp.groupby(["key_group","status_outlier"]).count().iloc[:,0]
df_tmp = df_outlier.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum())).reset_index().sort_values("key_group", ascending= False)

df_outlier = df_tmp["key_group"].str.split("|",expand=True)
df_outlier["dia"] = day_gregorate
df_outlier["status_outlier"] = df_tmp["status_outlier"]
df_outlier["pct_comparativo_mayo22"] = df_tmp["Time"]

df_outlier.columns = ["señal","grado_acero","velocidad_linea","ancho_slab","dia","status_outlier","pct_comparativo_mayo22"]
df_outlier = df_outlier[df_outlier["pct_comparativo_mayo22"] != 100]

#Cruze y outliers

fig = px.scatter(
    ddf_complete_tmp,
    x = "Time",
    y = "value", 
    color = "groupings",
    title = "Detalle de grupos por señal grado acero | velocidad linea | ancho planchon")

fig.show()

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
