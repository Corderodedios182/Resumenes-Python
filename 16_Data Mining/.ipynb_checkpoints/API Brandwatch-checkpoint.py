# -*- coding: utf-8 -*-
"""
Editor de Spyder
Este es un archivo temporal
"""
import pandas as pd
import requests
#---------------------------------------------------------------------------------------------------------------#
###############################
#Funciones de Apoyo Brandwatch#
###############################

#################################
#Token de Acceso para Brandwatch#
################################
def Brandwatch_Token(URL):
    r = requests.get(url = URL)
    Info = r.json()
    return Info

#######################################
#Extraccion de Datos Json a Data Frame#
#######################################
    
def Brandwatch_Datos(URL_Proyectos):
    r = requests.get(url = URL_Proyectos)
    Info = r.json()
    Resultados = Info['results'] #Tomamos la llave results y su contenido
    Resultados = pd.DataFrame(Resultados, columns=Resultados[0].keys())
    return Resultados