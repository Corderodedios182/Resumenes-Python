import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash import Output, Input

import dask.dataframe as dd

#Carga de datos
df = dd.read_csv('data/df_signal.csv').compute()

# Create the Dash app
app = dash.Dash(__name__)

# Set up the layout using an overall div
app.layout = html.Div(
    children=[
        dcc.Dropdown(id = 'title_dd',
                     options = [{'label':'signal 1',
                                'value':'hsa12_loopout_dsrsprtrdactpst_C1075052648'},
                                {'label':'signal 2',
                                 'value':'hsa12_loopout_eslsprtrdactpst_C1075052642'}
                                ]),
        dcc.Graph(id='my_graph')
        ])

@app.callback(
    Output(component_id = 'my_graph',
           component_property = 'figure'),
    Input(component_id = 'title_dd',
           component_property = 'value')
     )
def update_layouts(selection):

    title = 'None'
    if selection:
        title = selection
     
    bar_graph = px.histogram(data_frame = df,
                       x = title,
                       title=f'{title}')

    return bar_graph

if __name__ == '__main__':
    app.run_server()
    
