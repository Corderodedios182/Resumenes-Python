# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 14:40:45 2022

@author: cflorelu
"""

from settings import *

# Plotly graph objects to render graph plots
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
pio.renderers.default='browser'

def exploratoryDataframe(datos):
    
    df = datos.groupby(["QID","TEXTO_COMPARACION"]).agg({"TEXTO_COMPARACION":"count",
                                     "EVALUACION":["min","max","mean","sum"]}).reset_index()
        
    df.columns = ["QID","TEXTO_COMPARACION","conteo_eventos","min_evaluaciones","max_evaluaciones","mean_evaluaciones","sum_evaluaciones"]
    
    fig = px.bar(df,
                 x = "QID",
                 y = "conteo_eventos",
                 hover_data=['TEXTO_COMPARACION','min_evaluaciones', 'max_evaluaciones','mean_evaluaciones','sum_evaluaciones'],
                 color = "sum_evaluaciones",
                 width = 1600,
                 height = 700,
                 text = "sum_evaluaciones",
                 title = r"Cantidad de eventos : {} distribuidos en {} tópicos.".format(sum(df["conteo_eventos"]), df.shape[0]) )
    
    return fig.show()
