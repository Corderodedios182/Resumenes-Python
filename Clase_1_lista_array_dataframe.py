# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

#numpy, pandas (manipulacion de datos) 

#Fundamentos basicos

#Tipos de variables

a = 1.4 #Flotantes
a = int(a)
a = 1 #Entero
a = complex(1)
a = '1'
a = bool(1) #True/False
10 % 2 #Funcion modulo
strings = 'hola' #Caracteres
strings * 2
strings + ' ' + 'adios'
'a' in 'hola' #Se encuentra a en 

#Tipos de datos 

listas = [1,1,2,3,4,5]
tuplas = (1,2,3,4,5)
diccionarios = {'Nombres':1}

#Funciones

str(1)
type(a)
del tuplas
dir(listas)

#Metodos de listas Numericas
type(listas)
listas.index(3) #Posicion del numero 3
listas.count(1) #Conteo de numero 1
listas.append([6,7,8,9,0]) #Agrega un nuevo elemento a la lista
listas.extend([1,2,3,4]) #Concatena los elementos a diferencia de append que lo agrega como elemento

listas.remove(1) #Remueve un elemento especifico de la lista
del(listas[1]) #Elimina elemento 0 en la lista
listas.pop(1) #Elimina el elemento 0 en la lista

listas.reverse()
listas.count(2)
listas.sort()

#Metodos para caracter

listas = ['carlos','roberto']
'carlos'.upper()
'CARLOS'.lower()
'ahahahahahaha'.count('a')
'ahahahahahaha'.replace('a','e')
'   ahahahahahaha  '.strip()

#Seleccionar elementos de una lista
listas[5][0]
listas[2:]
listas[:2]
listas[-1]

#Seleccion del texto
lista_texto = ['carlos','robert','flores','luna']
lista_texto[0]
lista_texto[0][1]


#Numpy basico
import numpy as np

my_list = [1,2,3,4,5]
my_list = np.array(my_list)
my_list2 = np.array([[1,2,3,4,5],[6,7,8,9,0]])

my_list2[0,0]
my_list2[0,:] 
my_list2[:,0] 

my_list2.shape
my_list = np.append(my_list,1)
my_list = np.insert(my_list,1,10) #Iserta un 10 en el elemento 1
my_list = np.delete(my_list,1) #Elimina el elemento
np.mean(my_list2)

#Definicion de arrays

a = np.array([1,2,3,4,5]) #Una dimension
b = np.array([6,7,8,9,1])
b = np.array([(1,2),(3,4)]) #2 dimensiones
b = np.array([[(1,2),(2,4)] , [(4,5,),(6,7)] ]) #3 dimensiones

#Creacion de arrays
np.zeros((2,2))
np.ones((1,2,3))
np.arange(10,25,5)
np.linspace(0,2,9)
np.full((2,2),7)
np.eye(4)
np.random.random(10)
np.empty((3,2))

c = np.random.rand(10).reshape(5,2)

#Descripcion de arrays
c.shape #Ambos
len(c) #Renglones
c.ndim #Columnas
c.size
c.dtype
c.astype(int)
#Informacion de algun metodo
np.info(np.array)

#Operaciones aritmecicas
a = np.array([1,2,3,4,5]) #Una dimension
b = np.array([6,7,8,9,1])

a + b
a - b
a/b
a == b
a > b

np.equal(a,b)

np.multiply(a,b)
np.log(a)
np.sqrt(a)
np.exp(a)
np.sum(a)

a.sum()
a.min()
a.mean()

a[a > 2] #Seleccion condicional

#Ejemplo de velocidad entre numpy y python clasico
N = 100
M = 100

#Numpy
N, M = 100, 100
a = np.empty(10000).reshape(N,M)
b = np.random.rand(10000).reshape(N,M)
c = np.random.rand(10000).reshape(N,M)

%%timeit
for i in range(0,N):
    for j in range(0,M):
        a[i,j] = b[i,j] + c[i,j]

%%timeit
a = c + b

#Pandas
import pandas as pd

data = pd.read_csv('https://assets.datacamp.com/production/course_1639/datasets/austin_airport_departure_data_2015_july.csv',
                   header= 10,
                   sep = ',',
                   parse_dates = ['Date (MM/DD/YYYY)'],
                   index_col = 'Date (MM/DD/YYYY)')

data.head()
data.tail()
data.describe() 
data.info()
data.keys()
data.shape
data.index

columna = data.iloc[:,[1,13]] #Numerica
columna_lista = list(columna)

columna = data.loc[:,('Flight Number','DelayWeather(Minutes)')] #Nombres


#Bucle
a = 9
for i in range(10):
    print(i+1)

i = 0
i += 1


if a > 10:
    print('mayor que 10')
elif a < 10:
    print('no es mayor que 10')

while a < 10: #Se termina cuando es False
    a = a + 1
    print(a)

#Definicion de una funcion
def Suma(x,y):
    return x + y



















 


#Suma con un for de la matriz b y c

def suma(x,y):
    return x + y

suma_lambda = lambda x,y : x + y

import os

os.getcwd()
os.chdir('') #setwd
os.listdir() #elementos






















#Iportancion de datos

#Introduccion a pandas