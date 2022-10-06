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
df_comparative_sample = pd.read_csv("data/ddf_dash/df_comparative_sample.csv")
ddf_may = pd.read_csv("data/ddf_dash/ddf_may.csv")
ddf_may["Grado"] = ddf_may["Grado"].astype(int)
ddf_may["Velocidad"] = ddf_may["Velocidad"].apply(lambda x: round(x, 1))

ddf_may["key_group"] = ddf_may["signal"].astype(str) + " | " + \
                       ddf_may["Grado"].astype(str) + " | " + \
                       ddf_may["Velocidad"].astype(str) + " | " + \
                       ddf_may["Ancho"].astype(str)

df_dash = pd.read_csv("data/ddf_dash/df_dash.csv")
df_dash['day'] = pd.to_datetime(df_dash['day']).dt.floor("D")

df_ideal = pd.read_csv("data/ddf_dash/df_ideal.csv")

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
####################
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
        dcc.Dropdown(df_dash["signal"].unique(),
                     id ='list_signal',
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
    
    #Text
    html.Div([
        html.Div(
            [html.H6(id="n_days"), html.P("N° de días")],
            id="days",
            className="mini_container"),
        html.Div(
            [html.H6(id="n_signals"), html.P("N° Señales")],
            id="signals",
            className="mini_container"),
        html.Div(
            [html.H6(id="groups_may"), html.P("Grupos muestra Ideal")],
            id="group_may",
            className="mini_container"),
        html.Div(
            [html.H6(id="groups_day"), html.P("Grupos en días seleccionados")],
            id="group_day",
            className="mini_container"),
        html.Div(
            [html.H6(id="groups_found"), html.P("Grupos comparados")],
            id="group_found",
            className="mini_container"),
        html.Div(
            [html.H6(id="groups_no_found"), html.P("Grupos no comparados")],
            id="group_no_found",
            className="mini_container")
        ],
        id="info-container",
        className="row container-display"
        ),
    
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
def filter_dataframe(df_dash, input_country, list_signal, start_date, end_date):
    dff = df_dash[ (df_dash["country"].isin([input_country])) 
            & (df_dash.stack().str.contains('|'.join(list_signal)).any(level=0))
            & (df_dash["day"] >= start_date) & (df_dash["day"] <= end_date)]
    return dff

###################
# Create callbacks#
###################

# Selectors -> n_days
@app.callback(
    Output("n_days", "children"),
    [
     Input('input_country', 'value'),
     Input("list_signal", "value"),
     Input("day", "start_date"),
     Input("day", "end_date")
     ])
def update_n_days(input_country, list_signal, start_date, end_date):

    dff = filter_dataframe(df_dash, input_country, list_signal, start_date, end_date)
    return len(dff["day"].unique())

# Selectors -> n_signals
@app.callback(
    Output("n_signals", "children"),
    [
     Input('input_country', 'value'),
     Input("list_signal", "value"),
     Input("day", "start_date"),
     Input("day", "end_date")
     ])
def update_n_signals(input_country, list_signal, start_date, end_date):

    dff = filter_dataframe(df_dash, input_country, list_signal, start_date, end_date)
    return len(dff["signal"].unique())

# Selectors -> groups_may
@app.callback(
    Output("groups_may", "children"),
    [
     Input("list_signal", "value")
     ])
def update_groups_may(list_signal):

    return len(ddf_may[ddf_may.stack().str.contains('|'.join(list_signal)).any(level=0)]["key_group"].unique())

# Selectors -> groups_day
@app.callback(
    Output("groups_day", "children"),
    [
     Input('input_country', 'value'),
     Input("list_signal", "value"),
     Input("day", "start_date"),
     Input("day", "end_date")
     ])
def update_groups_day(input_country, list_signal, start_date, end_date):

    dff = filter_dataframe(df_dash, input_country, list_signal, start_date, end_date)
    return len(dff["key_group"].unique())

# Selectors -> groups_found
@app.callback(
    Output("groups_found", "children"),
    [
     Input('input_country', 'value'),
     Input("list_signal", "value"),
     Input("day", "start_date"),
     Input("day", "end_date")
     ])
def update_groups_found(input_country, list_signal, start_date, end_date):

    dff = filter_dataframe(df_dash, input_country, list_signal, start_date, end_date)
    
    keys_group_may22     = ddf_may[ddf_may.stack().str.contains('|'.join(list_signal)).any(level=0)]["key_group"].unique()
    keys_group_analyisis = dff["key_group"].unique()
    found = [item in list(keys_group_analyisis) for item in list(keys_group_may22)]
    
    return sum(found)

# Selectors -> groups_no_found
@app.callback(
    Output("groups_no_found", "children"),
    [
     Input('input_country', 'value'),
     Input("list_signal", "value"),
     Input("day", "start_date"),
     Input("day", "end_date")
     ])
def update_groups_no_found(input_country, list_signal, start_date, end_date):

    dff = filter_dataframe(df_dash, input_country, list_signal, start_date, end_date)
    
    keys_group_may22     = ddf_may[ddf_may.stack().str.contains('|'.join(list_signal)).any(level=0)]["key_group"].unique()
    keys_group_analyisis = dff["key_group"].unique()
    found = [item in list(keys_group_analyisis) for item in list(keys_group_may22)]
    
    return keys_group_analyisis.shape[0] - sum(found)

# Main table -> table_2
@app.callback(
    Output("table_2", "figure"),
    [
     Input('input_country', 'value'),
     Input("list_signal", "value"),
     Input("day", "start_date"),
     Input("day", "end_date")
    ])
def table_details_2(input_country, list_signal, start_date, end_date):
    
    dff = filter_dataframe(df_dash, input_country, list_signal, start_date, end_date)
    
    dff["key_group"] = dff["day"].astype(str) + dff["signal"]
    dff = dff[dff["indicator"] == 'revision']
    dff = dff.loc[:,["day","signal","indicator"]].drop_duplicates()
    dff.columns = ["dia","señal_a_revisar","indicator"]
    dff = dff.sort_values("señal_a_revisar")
    
    trace_0 = go.Table(
        header=dict(values=list(dff.columns),
                    fill_color='paleturquoise',
                    align='center'),

        cells=dict(values=[dff.dia,
                           dff.señal_a_revisar,
                           dff.indicator,
                           ],
                   fill_color='lavender',
                   align='center'))

    layout_0 = go.Layout(legend = {"x":.9,"y":.5},  margin=dict(l=20, r=20, t=20, b=20),
                         width=1600,
                         height = 200,
                         showlegend = False,
                         template = 'ggplot2',
                         )

    fig_1 = go.Figure(data = [trace_0], layout = layout_0)

    return fig_1

# Main table -> table_1
@app.callback(
    Output("table_1", "figure"),
    [
     Input('input_country', 'value'),
     Input("list_signal", "value"),
     Input("day", "start_date"),
     Input("day", "end_date")
    ])
def table_details(input_country, list_signal, start_date, end_date):
    
    dff = filter_dataframe(df_dash, input_country, list_signal, start_date, end_date)
    
    dff["key_group"] = dff["day"].astype(str) + dff["signal"]
    dff = dff.groupby(["key_group","day","signal","indicator"]).agg({"country":'count'})
    dff = dff.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum())).reset_index()#.sort_values("key_group", ascending= False)
    dff = dff.sort_values('country', ascending=False).groupby(["day","signal"], as_index=False).first().reset_index()
    dff = dff.loc[:,["day","signal","indicator","country"]]
    dff.columns = ["dia","señal","status_señal","porcentaje_status"]
    
    ddf_general = dff.groupby(["dia","status_señal"]).agg({"señal":"count"}).reset_index()
    ddf_general.columns = ["dia","status_señal","numero_señales"]
    ddf_general = ddf_general.pivot(index="dia", columns="status_señal", values="numero_señales").reset_index().fillna(0)
    ddf_general["dia"] = pd.to_datetime(ddf_general['dia']).dt.floor("D")
    
    if 'revision' not in ddf_general.columns:
        ddf_general["revision"] = 0
    
    if 'estable' not in ddf_general.columns:
        ddf_general["estable"] = 0
    
    if 'media' not in ddf_general.columns:
        ddf_general["media"] = 0
    
    trace_0 = go.Table(
        header=dict(values=list(ddf_general.columns),
                    fill_color='paleturquoise',
                    align='center'),

        cells=dict(values=[ddf_general.dia,
                           ddf_general.estable,
                           ddf_general.revision,
                           ddf_general.media
                           ],
                   fill_color='lavender',
                   align='center'))

    layout_0 = go.Layout(legend = {"x":.9,"y":.5},  margin=dict(l=20, r=20, t=20, b=20),
                         width=1600,
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
     Input("list_signal", "value"),
     Input("day", "start_date"),
     Input("day", "end_date")
    ])
def update_fig_bar(input_country, list_signal, start_date, end_date):

    dff = filter_dataframe(df_dash, input_country, list_signal, start_date, end_date)
    
    fig = go.Figure()

    tmp = dff.groupby(["signal","country","indicator"]).agg({"key_group":"count"})
    tmp = tmp.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum())).reset_index()
    tmp.columns = ["signal","country","indicator","porcentaje"]
    
    tmp = tmp.sort_values("indicator")
    
    fig = px.bar(tmp,
                 x="signal",
                 y="porcentaje",
                 color="indicator",
                 color_discrete_sequence=["green", "yellow", "red"],
                 width=1600,
                 height=700,
                 title="Status por señal")
    
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True,
                     ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=10, col=1)
    
    fig.update_xaxes(ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=4,
                     constrain="domain",showline=True, linewidth=2, linecolor='black', mirror=True)

    return fig

# Main graph -> graph scatter
@app.callback(
    Output(component_id = 'fig_1',
           component_property = 'figure'),
    [
     Input('input_country', 'value'),
     Input("list_signal", "value"),
     Input("day", "start_date"),
     Input("day", "end_date")
    ])
def update_fig_scatter(input_country, list_signal, start_date, end_date):

    dff = filter_dataframe(df_dash, input_country, list_signal, start_date, end_date)
    
    dff = dff.sort_values("indicator")
    dff["pct_val_no_zeros"] = dff["pct_val_no_zeros"]/100

    fig = go.Figure()
        
    fig = px.scatter(
        dff,
        x="pct_val_no_zeros",
        y="within_range", 
        color="indicator",
        color_discrete_sequence=["green", "yellow", "red" ],
        width=1600,
        height=700,
        facet_col="indicator",
        size='Cantidad_CU_may22', 
        hover_data=['key_group'],
        title="Detalle Indicadores : Completitud | Outlier | N° Casos Uso")
    
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True,
                     ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=10, col=1)
    
    fig.update_xaxes(ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=4,
                     constrain="domain",showline=True, linewidth=2, linecolor='black', mirror=True)
    
    return fig

# Main table -> data details
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df_ideal.to_csv, "información_detalle.csv", index=False)

# Main
if __name__ == "__main__":
    app.run_server(debug=True, 
                   use_reloader=False)
