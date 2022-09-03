# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 10:45:34 2022

@author: cflorelu
"""
from dash import Dash, dcc, html, Input, Output

#Creación de la app
app = Dash(__name__)

app.layout = html.Div([
    dcc.Input(id = 'mi-input', value = 'valor inicial', type = 'text'),
    html.Div(id='my-div')
])

@app.callback(
    Output('mi-salida','children'),
    [Input('mi-input','value')]
)
def actualizar_div(valor_entrada):
        
    return f'Has insertado la cadena : {valor_entrada}'

if __name__ == '__main__':
    app.run_server()





