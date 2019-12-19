# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 12:28:23 2018

@author: admin
"""

import os 
import zipfile
import pandas as pd
import numpy as np

os.getcwd()
os.chdir('C:/Users/admin/.kaggle/google-play-store-apps')
os.listdir()

Base = pd.read_csv(os.listdir()[0])
Base_1 = pd.read_csv(os.listdir()[1])

#Creacion array 

Array = np.array([range(1,5)])
Array = np.array([range(1,5),range(4,8)])
Array = np.array([[range(1,5),range(4,8)], [range(1,5),range(4,8)]], dtype = float)

    #Array iniciales

np.zeros((2,2))
np.ones((1,2,3))
np.arange(10,25,5)
np.linspace(0,2,9) 
np.full((2,2),7)
np.eye(5)
np.random.random((3,3))
np.empty((3,3))

    #Tipos de datos

np.int64
np.float32
np.complex
np.bool
np.object
np.string_
np.unicode_

#Inspeccion

Array_0 = np.ones((10841,13))
Array_1 = np.random.random((10841,13))

Array.shape
len(Array)
Array.ndim
Array.size
Array.dtype
Array.dtype.name

#Matematicas de Arrays

Nueva_0 = Array_0 - Array_1
Nueva = np.subtract(Array_0,Array_1)
Nueva_0 == Nueva

Nueva_0 = Array_0 + Array_1
Nueva = np.add(Array_0,Array_1)
Nueva_0 == Nueva

Division = np.divide(Array_0,Array_1)
Multiplicacion = np.multiply(Array_0,Array_1)
Exponencial = np.exp(Array_0)
Raiz = np.sqrt(Array_0)
Seno = np.sin(Array_0)
Coseno = np.cos(Array_0)
log = np.log(Array_0)

Division < Multiplicacion

#Funciones de Agregacion

Array_0.sum()
10841*13
Array_0.min()
Array_1.max(axis=0) #Maximo de cada fila
Array_0.cumsum(axis = 1) #Suma acumulativa por columna
Array_0.mean()
np.std(Array_0)

    #Copia de Arrays

C = Array_0.view()
np.copy(C)
C = Array_0.copy()

    #Ordenamiento

Array_1.sort() #Menor a mayor
Array_1.sort(axis = 1)

#Seleccion, corte, Indexacion

Array_1[0]
Array_1[0,0]

Array_1[0:2]
Array_1[0:2,0]
Array_1[:1]
Array_1[1,...]
Array_1[ : : -1]

    #Booleanos

Array_1[Array_1 > .5]

#Manipulacion de Arrays

t = np.transpose(Array_1)
t.T



















    















