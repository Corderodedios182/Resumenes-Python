# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 22:49:03 2022
@author: Carlos HEB
"""
import requests
import json
import pandas as pd
import os 
from datetime import date

#os.chdir("C:/Users/Carlos HEB/Documents/HBE/Web-Scraping")
os.listdir()

def extract_sucursales():
    
    sucursales_api = 'https://www.lacomer.com.mx/lacomer-api/api/v1/public/header/inicio?cambioSucc=false&succFmt=100&succId=439'
    sucursales_json = json.loads(requests.get(sucursales_api).text)['sucursalesGral']
    sucursales = pd.DataFrame(sucursales_json)
    
    return sucursales

def extract_depto(succId = 439) :
    
    """Listado de departementos y categorias"""
    deps_api = 'https://www.lacomer.com.mx/lacomer-api/api/v1/public/header/inicio?cambioSucc=false&succFmt=100&succId={}'.format(succId)
    deps_json = json.loads(requests.get(deps_api).text)['departamentos']
    deps_list = list(deps_json.keys())
    deps_df = []

    for depto in deps_list :
        
        tmp = pd.DataFrame(deps_json[depto])
        tmp['dept'] = depto
        deps_df.append(tmp)
        
    deps_df = pd.concat(deps_df)
    deps_df['dept'].unique()

    sucursales = extract_sucursales()
    deps_df['succId'] = succId
    deps_df['sucursal'] = sucursales.loc[sucursales['id'] == succId,'sucursal'].iloc[0]

    return deps_df

def extract_articulos(deps_df, succId = 439):

    """Listado de Articulos"""    

    agruIds = list(deps_df['agruId'].astype(int).unique())
    articulos_df = []

    for agruId in agruIds:
        articulos_api = 'https://www.lacomer.com.mx/lacomer-api/api/v1/public/articulopasillo/articulospasillord?filtroSeleccionado=0&idPromocion=0&marca=&noPagina=1&numResultados=20&orden=-1&padreId={}&parmInt=1&pasId=1&pasiPort=0&precio=&succId={}'.format(agruId,succId)
        articulos = json.loads(requests.get(articulos_api).text)['vecArticulo']
        articulos = pd.DataFrame(articulos)
        articulos_df.append(articulos)

    todos_articulos = pd.concat(articulos_df)

    todos_articulos = todos_articulos.loc[:,["artEan","artCod","artDes","marDes","artPrven","artPrlin","artProfe","artUco","artTun","artPvcap","agruId","artPres",
                           "artGranel","artEquiv","pasilloId","agruOrden","succId","inveCant","artImg","artBstop","promoCartulina","tipoPromo",
                           "articulosCompra","articulosPaga","porcentaje","descripcionSIMA","numPromoTimbres","normal_price","price_15_timb",
                           "price_30_timb","fichaTecnica","existeFichaTecnica","promocionTimbres"]]

    todos_articulos['fecha_extraccion'] = date.today()

    return todos_articulos

##############
#Extracciones#
##############
sucursales = extract_sucursales()
deps_df = extract_depto()
deps_df = deps_df.loc[:,['agruId', 'agruDes','totalArticulos','dept','succId', 'sucursal']]

todos_articulos = extract_articulos(deps_df, succId = 439)
#todos_articulos.to_csv('articulos_fresco_{}.csv'.format(date.today()))

#Validaciones
todos_articulos = todos_articulos.merge(deps_df, how = 'left', on = 'agruId')

#¿Cuantos arituclos por Departamento?
deps_df.groupby(['dept'],as_index=False).agg({'totalArticulos':'sum'}).sort_values('totalArticulos', ascending = False)['totalArticulos']
print("Porcentaje de Extraccion : " , 100 * (todos_articulos.shape[0] / sum(deps_df['totalArticulos'])))

#¿Cuantas categorias por Departamento?
deps_df.groupby(['dept'],as_index=False).agg({'agruDes':'count'}).sort_values('agruDes', ascending = False)

#Identificando Rebajados, NxN (3x2), 2x150 ahormaces 2xprecio_x
todos_articulos.columns

todos_articulos.rename(columns={'artPrlin': 'precio_base','artPrven':'precio_rebajado'}, inplace=True)
todos_articulos['rebaja'] = todos_articulos['precio_base'] - todos_articulos['precio_rebajado']  
todos_articulos.loc[todos_articulos['rebaja'] != 0, 'Promocion_rebaja'] = 'Rebaja'

#Analisis de los tipos de rebajas y no rebajas si tienen grupos de Promociones
todos_articulos['tipoPromo'].value_counts()
todos_articulos.groupby(['tipoPromo','articulosCompra','articulosPaga','porcentaje'], as_index = False).count().iloc[:,:5]
promociones = todos_articulos.groupby(['tipoPromo','articulosCompra','articulosPaga','porcentaje','descripcionSIMA','promoCartulina'], as_index = False).count().iloc[:,:7]

#1 -> NxN
#2 -> Monedero
#3 -> Llevate

todos_articulos.loc[todos_articulos['tipoPromo'] == 1, 'Promocion'] = 'NxN'
todos_articulos.loc[todos_articulos['tipoPromo'] == 2, 'Promocion'] = 'Monedero'
todos_articulos.loc[todos_articulos['tipoPromo'] == 3, 'Promocion'] = 'Llevate'
todos_articulos['Promocion'] = todos_articulos['Promocion'].fillna('no tiene')

todos_articulos['Promocion_NxN'] = todos_articulos['articulosCompra'].map(str) + ' x ' + todos_articulos['articulosPaga'].map(str) + '.' +  todos_articulos['porcentaje'].map(str)

#Categorias validacion
barberia = todos_articulos[todos_articulos.agruId == 909]
harinas_arroz_leumbres = todos_articulos[todos_articulos.agruId == 67]
bebidas_lacteos = todos_articulos[todos_articulos.agruId == 27]

#Agrupaciones validaciones
todos_articulos['tipoPromo'].value_counts()
todos_articulos.groupby(['tipoPromo','articulosCompra','articulosPaga','porcentaje'], as_index = False).count().iloc[:,:5]
promociones = todos_articulos.groupby(['tipoPromo',"Promocion",'Promocion_NxN','agruDes','agruId'], as_index = False).count().iloc[:,:6]
promociones = todos_articulos.groupby(['tipoPromo','articulosCompra','articulosPaga','porcentaje','descripcionSIMA','promoCartulina','Promocion','Promocion_NxN'], as_index = False).count().iloc[:,:8]

#Extraccion Vigencias
#Identificar los Llevate como promociones

#/d gigito, D/ no-digito /s espacio, S/ no-espacio , /w caracter de palabra, /W no-caracter de palabra caracter especial ejemplo #

llevate = promociones[promociones['Promocion'] == 'Llevate']

import re
numeros = {"UNO":1,"DOS":2,"TRES":3,"CUATRO":4,"CINCO":5,"SEIS":6,"SIETE":7,"OCHO":8,"NUEVE":9,"DIEZ":10}

llevate['tmp'] = llevate['promoCartulina'].str.findall(r'(?:LLEVATE|LLEVA|LEVATE+)\s(\w+)')
llevate['tmp'] = [x[0] for x in llevate['tmp']]
llevate['tmp'] = llevate['tmp'].replace(numeros)

llevate['tmp_1'] = llevate['promoCartulina'].str.findall(r'(?:POR+)\s(\d+)')
llevate['tmp_1'] = [x[0] for x in llevate['tmp_1']]

llevate['tmp_2'] = llevate['tmp'] + llevate['tmp_1']
