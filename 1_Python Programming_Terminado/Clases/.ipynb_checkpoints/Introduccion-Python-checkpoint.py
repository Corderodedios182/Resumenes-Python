# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 16:53:44 2020

@author: crf005r
"""

    #################
    #¿Que es Python?#
    #################

    #Es un lenguaje de programacion Orientado a Objetos, programacion imperativa, programacion funcional.
    
    #   - Con una sintaxis sencilla de entender y aprender.
    
    #   - Ampliamente utilizado en Ciencia e Ingenierias
    
    #   - Multiples bibliotecas

    ##############################################
    #Variables Numericas y operaciones habituales#
    ##############################################

1 + 1 #suma
2 - 2 #resta
1 / 2 #division
1 * 2 #multiplicacion
2**2 #exponente

a = 0 #asignacion de variables
b = 2 

a != b #Condicionales logicas (distinto de)
a > b #mayor que
a < b #menor que
a == b #igual 

#funciones
int(1.5)  #funcion para convertir un numero con decimales en entero
round(1.5) #redondear un numero 
abs(-1.5) #valor absoluto 
sum([a,b]) #sumar 2 variables numericas

a = 10 #asignacion de variables
b = 10.00 

type(a) == type(b) #comparar el tipo de datos

    ##############################
    #Tipos de Variables en Python
    #int - numeros enteros
    #float - numeros flotantes
    #complex - numeros complejos
    #bool- Verdaderos o Falsos booleanos
    #str - caracteres
    #lis - listas
    #tuple - tuplas
    #dict - diccionario
    #dataframes - "datos estructurados"
    ##############################

    # - str (characteres)

a = '  Hola!! ' #asignar una variable un caracter
a
a + 'Carlos' #concatenar texto con el signo +
a + input(' ¿Como te llamas? : ') #pedir al usuario que ingrese un texto

a * 5 #repite 5 veces los caracteres de la variable a

type(a) #tipo de datos

#metodos que tiene la variable a (al ser un caracter tiene sus propios metodos)
a.lower() #convierte en minusculas 
a.upper() #convierte a mayusculas
a.rstrip() #elimina espacio derecho
a.strip() #elimina entre espacions

help(str.lower) #funcion de ayuda para ver los metodos de los tipos de datos caracteres
help(str.capitalize) 

help(sum) 

"Colocamos lo que deseamos como {} podemos colocar varias cosas {}".format(":)", "en cada corchete {}")
"Tambien {variable} podemos nombrar las variables {valor}".format(variable = "ÑLKJADSF", valor = "123")

# Import datetime 
from datetime import datetime #Importando la paqueteria datetime

get_date = datetime.now() #hora actual
get_date

message = "Good morning. Today is {today:%B %d, %Y}. It's {today:%H:%M} ... time to work!" #en el contenido de los corchetes {} asignaremos un valor. 
message.format(today=get_date) # donde tenemos la palabra today asignara el valor de get_date

"I believe you I always said that the actor actor...".find("eve") #Busca la palabra y marca su comienzo
"I believe you I always said that the actor actor...".replace("actor","actores") #Remplaza actor por actores
"I believe you I always said that the actor actor...".replace("actor","actores").count("actores") #Conteo de palabras

    # - list (Lista)
    #Listas; Las listas son conjuntos ordenados de elementos (números, cadenas, listas, etc).
    #Las listas se delimitan por corchetes ([ ]) y los elementos se separan por comas.

print(' "hola" ') #Imprime Hola

lista = [1, 4, 'Python', [7,10], 2 ] #definicion de una lista
lista = list(range(0,10,1))
lista = list(range(0,10,1))
lista + 1 
np.arange(10) + 1

len(lista) #longitud de una lista

lista[0] #seleccion del elemento 0
lista[3] #seleccion del elemento 3
lista[-1] #seleccion del elemento -1
lista[:] #selecciona todos los elementos
lista[3][1] #selecciona el elemento 3 la cual es una sublista y luego el emento 1
lista[:2] #selecciona hasta el elemento 2
lista[2:] #selecciona del elemento 2 en adelante

#Imprimiendo los elementos de la lista
for elementos in lista:
    print(elementos)

#metodos de la lista
lista.append(1) #añade registro
lista.clear() #limpia listas
lista.count(1) #cuenta 
lista.extend([1]) #agrega
lista.index(1) #da posicion
lista.remove(1) #remueve 
lista.reverse() #voltea

#Como utilizaremos las listas.
import pandas as pd #libreria para trabajar con DataFrames
import numpy as np  #libreria para trabajar con matrices
import matplotlib as mplt #libreria para graficar

People_List = ['Jon','Mark','Maria','Jill','Jack'] #definimos una lista
pd.DataFrame(People_List,columns=['First_Name']) #convertimos una lista a DataFrame

People_List = [['Jon','Smith',21],['Mark','Brown',38],['Maria','Lee',42],['Jill','Jones',28],['Jack','Ford',55]] #definicion de una lista con sublistas
pd.DataFrame(People_List,columns=['First_Name','Last_Name','Age']) #convertimos una lista a DataFrame

People_List = [['Jon','Mark','Maria','Jill','Jack'],['Smith','Brown','Lee','Jones','Ford'],[21,38,42,28,55]] #definicion de una lista
df = pd.DataFrame(People_List).transpose() #transponemos el DataFrame
df.columns = ['First_Name','Last_Name','Age'] #cambio del 
df

print ('People_List: ' + str(type(People_List)))
print ('df: ' + str(type(df)))

mean1 = df['Age'].mean()
max1 = df['Age'].max()
min1 = df['Age'].min()

print ('The mean age is: ' + str(mean1))
print ('The max age is: ' + str(max1))
print ('The min age is: ' + str(min1))

df.describe()
df.info()

df['Age'] = df['Age'].astype(int)

df.describe()
df.info()

df = pd.DataFrame(People_List, index = ['First_Name','Last_Name','Age'],columns = ['a','b','c','d','e'])

df.index

    # - tuple (Secuencia de objetos inmutables)

tupla =  ( 1, 4, 'Python', [7,10], 2 )
lista = [1, 4, 'Python', [7,10], 2 ]

tupla.count(1)

lista == tupla

#Diferencia entre tupla y lista, unas son estaticas y las otras dinamicas.
    
    # - dict (Diccionario)
    #Diccionario; Un Diccionario es una estructura de datos y un tipo de dato en Python 
    #con características especiales que nos permite almacenar cualquier tipo de valor
    #como enteros, cadenas, listas e incluso otras funciones.
    #Estos diccionarios nos permiten además identificar cada elemento por una clave (Key).

#Definicion de un Diccionario

diccionario = {'nombre':'Carlos',
               'edad':25,
               'cursos':['Python','R','Django','Jupyter']}

#Accediento a los elementos de la llave cursos
diccionario['cursos']
diccionario.pop('cursos')
diccionario.items()
diccionario.keys()
diccionario.values()

#Diccionarios de diccionarios, Los podemos interpretar como un base de datos en la que tenemos el nombre de las columnas y filas.

europe = { 'spain': { 'capital':'madrid', 'population':46.77 },
           'france': { 'capital':'paris', 'population':66.03 },
           'germany': { 'capital':'berlin', 'population':80.62 },
           'norway': { 'capital':'oslo', 'population':5.084 } }

print('Estructura de un Diccionario dentro de un Diccionario: ', europe)

print('Capital de Francia: ',europe['france']['capital']) #Seleccion de la capital que se encuentran en France

import pandas as pd

pd.DataFrame(europe)

#Agregacion de un Diccionario a un Diccionario
data = { 'capital':'rome', 'population':59.83 } #Creacion de un Diccionario

europe['italy'] = data 

#Creacion de Data Frames
#Tienen una estructura tabular (Base de datos)

names = ['United States', 'Australia', 'Japan', 'India', 'Russia', 'Morocco', 'Egypt']
dr =  [True, False, False, False, True, True, True]
cpc = [809, 731, 588, 18, 200, 70, 45]

#Definimos las Columnas y rellenamos con la listas (names,dr,cpc)
my_dict = { 'country':names, 'drives_right':dr, 'cars_per_cap':cpc }
cars = pd.DataFrame(my_dict)
print(cars)
type(cars)

row_labels = ['US', 'AUS', 'JAP', 'IN', 'RU', 'MOR', 'EG'] #Creamos una lista que sera el nombre de nuestras filas
cars.index = row_labels #Coloca nombres a las Filas
print(cars)

cars.info()
cars.describe()

cars['nueva_columna'] = cars['cars_per_cap']*10
cars

    #- DataFrames

mtcars = pd.read_csv("C:/Users/crf005r/Documents/mtcars.csv", index_col = 0)
mtcars.head()
mtcars.info()
mtcars.isnull().all()
mtcars.index
mtcars.shape
mtcars.keys()
mtcars.columns
type(mtcars)

mtcars[ ['cyl','mpg'] ] #Seleccion de Columnas del DataFrame mtcars
mtcars[0:3] #Seleccion de Filas

mtcars.iloc[2] #Selecion de filas con la funcion .iloc
mtcars.loc[['Datsun 710', 'Toyota Corona']] #Seleccion por el nombre de la fila funcion .loc

mtcars.iloc[5, 2] #Fila 5 columna 2
mtcars.loc[['Datsun 710', 'Toyota Corona'], ['cyl', 'qsec']] #Fila y columna por nombre

mtcars.iloc[:, 2] #Toda la fila 2 con Tipo de datos Series
mtcars.iloc[:, [2]] #Toda la fila 2 con Tipo de datos dataFrame
mtcars.loc[:, ['disp', 'cyl']] #Columnas con Tipo dataFrame

mtcars[mtcars["mpg"] > 21]

mtcars[(mtcars["mpg"] > 21) & (mtcars["cyl"] == 4)]
mtcars[(mtcars["mpg"] > 21) | (mtcars["cyl"] == 4)]

mtcars["cyl"].value_counts()
mtcars.groupby(["cyl"]).count()
mtcars.groupby(["cyl"]).count()["mpg"]


    ##########
    #Paquetes#
    ##########
    
    #Los paquetes son un conjunto de modulos, los modulos son archivos de codigo .py con variables, funciones y otros objetos.
    
    #En Python, cada uno de nuestros archivos .py se denominan módulos. Estos módulos, a la vez, pueden formar parte de paquetes.
    #Un paquete, es una carpeta que contiene archivos .py. Pero, para que una carpeta pueda ser considerada un paquete, debe contener un archivo de inicio llamado __init__.py. Este archivo, no necesita contener ninguna instrucción. De hecho, puede estar completamente vacío.
    
    #└── paquete 
    #    ├── __init__.py 
    #    ├── modulo1.py 
    #    ├── modulo2.py 
    #    └── modulo3.py
    # Los paquetes, a la vez, también pueden contener otros sub-paquetes:
     
    #└── paquete 
    #    ├── __init__.py 
    #    ├── modulo1.py 
    #    └── subpaquete 
    #        ├── __init__.py 
    #        ├── modulo1.py 
    #        └── modulo2.py
    
    #Y los módulos, no necesariamente, deben pertenecer a un paquete:
    
    #├── modulo1.py 
    #└── paquete 
    #    ├── __init__.py 
    #    ├── modulo1.py 
    #    └── subpaquete 
    #        ├── __init__.py 
    #        ├── modulo1.py 
    #        └── modulo2.py
    
    #Numpy es un ejemplo de paquete en Python.
    
    # ¿Que es Numpy?
    
    # Es una paqueteria de python, sirve para facilitar la manipulacion de vectores y matrices.
    
    #Motivacion para Usar numpy.
    
    #   - Los bucles son costosos
    
    #   - Eliminar bucles, vectorizar operaciones
    
    #   - Los bucles se ejecutan en python, las operaciones vectorizadas en C
    
    #   - Las operaciones entre arrays de NumPy se realizan elemento a elemento.

import numpy as np

np.arange(100)

np.e
np.pi
np.log(2)
np.arange(10) + 1

# Arrays de NumPy

# ¿Que es un Array?

# Una de las estructuras de datos más fundamentales en cualquier idioma es el arrays (matriz).

# Python no tiene una estructura de datos de matriz nativa, pero tiene una lista que es mucho más general y se puede usar como un arrays (matriz), multidimensional con bastante facilidad.

np.array([1,2,3,4], dtype = str)
np.array([1,2,3,'1'], dtype = float)

a = np.array([ [1,2,3], [2,4,6] ])
a[0]
a[0,0]
a[0,0:2]

# Ventajas de trabajar con arrays y paquetes.

cpc = [809, 731, 588, 18, 200, 70, 45] #Lista
cpc[cpc>150] #genera un error, no puedes operar asì con listas

cpc_array = np.array([cpc]) #Convertimos a array
cpc_array[cpc_array>150] # Convirtiendo a array puedes hacer filtros, eg de mayores a 150

a = mtcars['mpg']
entre = np.logical_and(a > 21, a < 40)
mtcars[entre]

a = 18 
np.logical_and(a < 18, a < 17) 
not(a < 18 and a < 17) #Negacion de la condicion

# Sumaremos dos matrices (b y c) almacenando los resultados en una tercer matriz llamada a

# Y veremos el tiempo que toma hacerlo de dos maneras diferentes

#Definicion de las matrices a,b y c
#Forma 1
N, M = 100, 100
a = np.empty(10000).reshape(N,M)
b = np.random.rand(10000).reshape(N,M)
c = np.random.rand(10000).reshape(N,M)

%%timeit #Mide el tiempo que tarda en ejecutar el codigo
#Suma elemento a elemento
for i in range(N):
    for j in range(M):
        a[i,j] = b[i,j] + c[i,j]
        
#Forma 2
%%timeit 
a = b + c #Esta operacion se realiza elemento a elemento y se encuentra mas optimizado.

    ####################################################
    #Condiciones logicas (if,else,while) y ciclos(for).#
    ####################################################

a = 5

#if, else, ifelse
if (a == 10):
    print("Verdadero")
else:
    print("Falso")

#
if(a < 4) :
    print("small")
elif(a < 6) :
    print("medium")
else :
    print("large")
    
#While (Termina de ejecutarse cuando la condicion es falsa)
offset = -6

while offset != 0 :
    print("correcting...")
    if offset > 0 :
        offset = offset - 1
    else :
        offset = offset + 1
    print(offset)

#for (Son ciclos para repetir acciones)
#Los for tienen la misma logica pero se debe tener en cuenta sobre el tipo de Objeto que se va a ejecutar.
#for lista simple
numeros = [1,2,3,4,5]

numeros[0] + 1

for i in numeros:
    print(i + 1)

areas = [11.25, 18.0, 20.0, 10.75, 9.50]

for index, area in enumerate(areas) :
    print("room " + str(index + 1) + ": " + str(area))
    
#for en listas compuesta   
house = [["hallway", 11.25], 
         ["kitchen", 18.0], 
         ["living room", 20.0], 
         ["bedroom", 10.75], 
         ["bathroom", 9.50]]
         
for x in house :
    print("the " + str(x[0]) + " is " + str(x[1]) + " sqm")    

#for en array
type(house)
house = np.array(house)
type(house)

for x in np.nditer(house):
    print(x)

#for en data frames
for x,y in cars.iterrows():
    print(x)
    print(y) #Imprime todos los datos por fila

for x, y in cars.iterrows():
    print(x + ":" + str(y["cars_per_cap"])) #Imprime los datos de una sola columna
    
for lab, row in cars.iterrows() :
    cars.loc[lab, "COUNTRY"] = row["country"].upper() #Convertimos los datos de country con mayusculas en la funcion upper()
    
cars["COUNTRY"] = cars["country"].apply(str.upper) #Realizamos el mismo proceso que el for con la funcion apply()
    
    ######################################################################################
    #Casos y Aplicaciones.                                                               #
    #Convinando todo lo anterior, desarrollaremos una grafica de una caminata aleatoria. #
    ######################################################################################
    
#Antes de comenzar es necesario conocer las funciones que nos ayudan a generar numeros aleatorios.
import numpy as np 
np.random.rand() #Numero Aleatorio
np.random.seed(123) #Semilla para generar el mismo numero
aleatorio = np.random.randint(0,10) #Numero aleatorio entre 0 y 10
step = 5

#If para ajustar el valor de una variable a partir de valor aleatorio que conseguimos anteriormente.
if aleatorio == 5:
    step = step - 1
elif aleatorio < 5:
    step = step
else :
    step = step + np.random.randint(0,10)
    
print(step)

#Caminatas aleatorias

#Para crear la caminata aleatoria, utilizamos un for anhidado.
#Como buena practica primero entendemos el for que se encuentra adentro.

import matplotlib.pyplot as plt
import numpy as np

np.random.seed(123)

Todas = []

for i in range(50):
    
    caminata_aleatoria = [0]

    for x in range(100):
    
        paso = caminata_aleatoria[-1]
    
        aleatorio = np.random.randint(1,7)
    
        if aleatorio <= 2:
             paso = max(0, paso - 1)
        elif aleatorio <= 5:
             paso = paso + 1    
        else:
             paso = paso + np.random.randint(1,7)
             
        if np.random.rand() <= 0.001:
            paso = 0
        
        caminata_aleatoria.append(paso) #Agregar el numero que se creo

        Todas.append(caminata_aleatoria)

#Al terminar de correr obtenemos una caminata aleatoria el cual nombraremos Todas

#Graficaremos los resultados obtenidos.
np_Todas = np.array(Todas) #Convertimos en array el objeto Todas
plt.plot(np_Todas)
plt.show()
plt.clf()

np_Todas_transpuesta = np.transpose(np_Todas)
plt.plot(np_Todas_transpuesta)
plt.show()

Final = np_Todas[-1,:]
plt.hist(Final)
plt.show()

np.mean(Final[Final > 30]) #Calculo de la media de datos que se ecuentran en la cola de datos aleatorios con un valor mayor a 30

    ################################
    #Definicion simple de funciones#
    ################################

#Primera Parte:
#Definicion de Funciones
def Saludo(Saludo,Frase):
    A = Saludo + '!'*3 + Frase + '.'*3
    return A

#Utilizando la Funcion que creamos
Saludo('Hola','¿Como estas?')

#Funcion con Multiples Parametros
def Saludo(Saludo,Frase):
    A = Saludo + '!'*3
    B = Frase + '.'*3
    Junto = (A,B)
    return Junto

#Funcion año biciesto
year = 1992

def is_leap(year):
        
    if ( year % 4 == 0  ):
         
        if ( (year % 100 != 0) | (year % 400 == 0) ):
            
            leap = True
        
        else: leap = False
    
    else:
        
        leap = False
    
    # Write your logic here
    
    return leap


is_leap(year)

#más simple
def is_leap_year(year):

    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

#Asignacion de Multiples Valores
Saludo('Hola','¿Como estas?')

    #¿Que sigue?
    #Herramientas utiles
    #Fundamentos Pandas
    #Analisis exploratorio
    
    ###########
    #Ejercicio#
    ###########
    
    #Busca una fuente de informacion e importar los datos en Spyder.
    #Puedes ocupar alguna de las siguientes 2 formas. E intenta contestar las siguientes preguntas...
    
    #1. ¿Que tipo de variables tienes?
    #2. Selecciona algunas columnas de interes
    #3. Crea un filtro
    #4. Cuenta los valores de una variable categorica

#########
#Forma 1#
#########
#Paquetes
import pandas as pd #Librería manipulacion de datos
import pyodbc #Conexión con ODBC
import sqldf #Libreria de python que nos ayuda a introducir codigo SQL

#En caso de tener un archivo csv o excell estas funciones te seran utiles, recuerda los parametros necesarios para una correcta lectura.
help(pd.read_csv)

base = pd.read_csv()
base = pd.read_excel()

#########
#Forma 2#
#########

#En caso de querer hacer una conexion directa con alguna base de datos.
import pandas as pd #Librería manipulacion de datos
import pyodbc #Conexión con ODBC
import sqldf #Libreria de python que nos ayuda a introducir codigo SQL

pd.options.display.float_format = '{:.2f}'.format

#Conexion
pyodbc.pooling = False
connection = pyodbc.connect("DSN=WMG; UID=crf005r; PWD=")

dc_dim = pd.read_sql_query("SELECT * FROM WW_CORE_DIM_VM.DC_DIM", connection) #Información de Cedis (12940 registros)

#Easter Egg
import this

import antigravity




