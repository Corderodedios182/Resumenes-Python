# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 16:09:35 2021

@author: Maste
"""

#¿Que es machine learning?

#Es la ciencia y el arte de darles a las computadoras capacidad de aprender a tomar decisiones a partir de datos sin ser programado explícitamente.

#Ejemplos:

#Tenemos etiquetas -> Aprendizaje Supervisado

    #Nuestra computadora puede aprender a predecir si un correo electrónico es spam o no dado su contenido y remitente.

#No tenemos etiquetas -> Aprendizaje No Supervisado -> La escencia de este metodo es descubrir patrones y estructuras ocultas a partir de datos sin etiquetar.

    #Clasificación de entradas de Wikipedia en función de las palabras que contienen. Luego cada artículo nuevo puede ser asignado a uno de los grupos existentes.
    
    #Clasificación de clientes 
    
#Aprendizaje Por Refuerzo -> Maquinas o Agentes interactúan con un entorno, los agentes de refuerzo pueden descubrir automáticamente cómo optimizar su comportamiento dado un sistema de recompensas y castigos.

    #Aplicaciones en Economía, Genética, Videojuegos.
    
    #2016 se ocupo para entrenar a Google DeepMind

    #AlphaGo

#########################
#Aprendizaje Supervisado#
#########################

#Tenemos varios puntos de datos o muestras descrito usando variables o características predictoras y una variable objetivo.

#Ejemplo la tabla iris: Variables predictoras (Sepal, Petal) y Variable Objetivo (Species)

#El objetivo del aprendizaje supervisado es construir un modelo que pueda predecir la variable objetivo.

    #Clasificación: Variable objetivo consiste en definir una categoría.
    
        #Predecir la Especie de una flor apartir de sus medidas de Sepal Y Petal.
    
    #Regresion: Variable objetivo es continua.

        #Precio de una casa.
        
 #Nota: Features = predictor variables = independent variables 
 
       #Target variable = dependent variable = response variable

#El objetivo del aprendizaje supervisado es con frecuencia automatizar una tarea manual costosa o que lleva mucho tiempo, como:

    #Un diagnóstico médico
    
    #Predicciones sobre el futuro
    
    #Si un cliente hará un clic en un anuncio
    
    
#Para el aprendizaje supervisado, necesitamos datos etiquetados y hay muchas formas de obtenerlos.

    #Datos historico ya etiquetados
    
    #Experimentos para obtener datos etiquetados, como pruebas A/B 
    
    #Datos etiquetados de colaboración colectiva
    
#En cualquier caso, el objetivo es aprender de los datos para los que se obtiene la salida correcta y podamos hacer predicciones sobre nuevos datos para los que no conocemos el resultado.

#Existen muchas maneras de hacer Aprendizaje Supervisado con Python.

#Utilizaremos scikit-learn, una de las bibliotecas más populaes y fáciles de usar para Python.

    #Se integra muy bien con SciPy Y Numpy
    
    #Existen otras bibliotecas como Tensorflow y Keras pero lo recomendable es familiarizarze con Scikit-Learn primero.
    

#Classification

#Regression

#Fine-tuning your model

#Preprocessing and pipelines

import os
os.listdir()
os.chdir("C:\\Users\\Maste\\Documents\\1_Github\\Resumenes-Python\\4_Machine Learning Scientist")
         #"C:\\Users\\crf005r\\Documents\\3_GitHub\\Resumenes-Python\\4_Machine Learning Scientist"
         

import matplotlib.pyplot as plt 
import plot_classifier as plt_cls
import pandas as pd
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier 

plt.style.use('ggplot')

#Podemos cuidar el tamaño de nuestras gráficas en los cuadernos jupyter
plt.rcParams['figure.figsize'] = [25, 8]

######################
#Conociendo los datos#
######################

#Trabajaremos con un conjunto de datos obtenido del Repositorio de Aprendizaje Automático de la UCI que consta de los votos hechos por los Congresistas de la Cámara de Representantes de EE. UU.

#El objetivo será predecir la afiliación partidaria ('demócrata' o 'republicano') en función de cómo votaron sobre ciertos temas clave.

#Aquí, vale la pena señalar que hemos preprocesado este conjunto de datos para tratar con los valores faltantes.

df = pd.read_csv('https://assets.datacamp.com/production/repositories/628/datasets/35a8c54b79d559145bbeb5582de7a6169c703136/house-votes-84.csv')

df.columns = ['party', 'infants', 'water', 'budget', 'physician', 'salvador','religious', 'satellite', 'aid', 
              'missile', 'immigration', 'synfuels','education', 'superfund', 'crime', 'duty_free_exports', 'eaa_rsa']

df.head()

base = df

#Limpiando los datos convertiremos los signos "?" en 0 
base.head()

#Tenemos 17 proyectos de ley y 434 democratas y republicanos, más adelante realizaremos un análisis exploratorio antes de proponer un modelo de clasificación

#Proyectos de ley
columna = base.iloc[:,1:].keys()
columna

#En ocasiones no todos los congresistas votan, colocando un signo "?", veremos más adelante como trabajar con este tipo de datos faltantes.

def conteo_tmp(base,columna = 'infants'):
    
    return base.loc[:,columna].value_counts()

pd.DataFrame( [conteo_tmp(base, columna[i]) for i in range(0,len(columna))] )

#Convertiremos los no = 0 y yes = 1, para tener variables dicotomicas.

# Conteo de democrat y republican

df.party.value_counts()

def remplazo(base,columna = 'infants'):
    base.loc[base.loc[:,columna] == 'y',columna] = 1
    base.loc[base.loc[:,columna] == 'n',columna] = 0
    base.loc[base.loc[:,columna] == '?',columna] = 0 #lo remplazaremos más adelante
    
    return base

for i in range(len(columna)):
    remplazo(base, columna[i])

base.head()

#Nuevo conteo con los no = 0 y yes = 1
pd.DataFrame( [conteo_tmp(base, columna[i]) for i in range(0,len(columna))] )


#Algunas Graficas proyecto de ley

plt.figure()
sns.countplot(x='education', hue='party', data=base, palette='RdBu')
plt.title("Votos para la educación, los democratas apoyaron más los proyectos de ley para educación")
plt.xticks([0,1], ['No', 'Yes'])
plt.show()


# Convertimos todo en una nueva base donde en una columna tenemos el partido, en otra todos los proyectos y las votaciones
base_melt = pd.melt(base.iloc[:,:5], id_vars = "party")

base_melt.variable.value_counts()

base_melt.head(15)

base_melt.party = base_melt.party.astype("category")
base_melt.variable = base_melt.variable.astype("category")
base_melt.info()

#Conteo de votos para algunas leyes
tmp = pd.DataFrame(base_melt.groupby(['party','variable','value']).size()).reset_index()
tmp.columns = ['party','variable','value','votos']
tmp

#################################################
#Modelo k-Nearest Neighbors: Fit (Clasificación)#
#################################################

#Habiendo explorado el conjunto de datos de los registros de votación del Congreso, es hora de construir su primer clasificador.

#En este ejercicio, ajustará un clasificador k-Nearest Neighbours al conjunto de datos de votación, que una vez más se ha cargado previamente en un DataFrame base.

# Creamos los datos separando la variable de respuesta
y = base['party'].values
X = base.drop('party', axis=1).values

lb_make = LabelEncoder()
y = lb_make.fit_transform(y)

# Instanciando un k-NN con n_neighbors = 6
knn = KNeighborsClassifier(n_neighbors=6)

# Entrenando los datos
knn.fit(X, y)

#Toma un vector del mismo tamaño que el numero de proyectos o culumnas
knn.predict(X)[0:10]

new_prediction = knn.predict([[0.696469, 0.286139,  0.226851 , 0.551315 , 0.719469 , 0.423106 , 0.980764, 0.68483,  0.480932,  0.392118,  0.343178,  0.72905,  0.438572,  0.059678, 0.398044,  0.737995]])
print("Prediction: {}".format(new_prediction)) 

#¿Como medimos el rendimiento de nuestro clasificador?

#En los problemas de clasificación, la presición es un métrica de uso común

#Lo que realmennte interesa es como el modelo va a responder a nuevos datos que nunca ha visto antes.

#Por esta razón, dividiremos el conjunto de datos en entrenamiento y pruebas.

#Entrenamos el modelo con los datos de entrenamiento y con el conjunto de pruebas hacemos nuevas predicciones y comparamos.

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 21, stratify = y)

knn = KNeighborsClassifier(n_neighbors=8)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)

#Para comprobar la presición de nuestro modelo, utilizamos el método de puntuación del modelo.
knn.score(X_test, y_test)

#Regiones de desición variando los parametros
plt.rcParams['figure.figsize'] = [20, 20]
plt.title("Knn región de desición líneal")
plt_cls.plot_decision_boundaries(X, y,  KNeighborsClassifier,n_neighbors=2)
plt_cls.plot_decision_boundaries(X, y,  KNeighborsClassifier,n_neighbors=8)
plt_cls.plot_decision_boundaries(X, y,  KNeighborsClassifier,n_neighbors=15)

#Grafica variando el numero de n_neighbors y su presición.
n_neighbors = range(1,20)
train  = []
test = []

for i in n_neighbors:
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train, y_train)
    
    train.append(knn.score(X_train, y_train))
    test.append(knn.score(X_test, y_test))

plt.rcParams['figure.figsize'] = [5, 5]
line_up, = plt.plot(n_neighbors, train , label='Training Accuracy')
line_down, = plt.plot(n_neighbors, test, label='Testing Accuracy')
plt.title("KNN : Variación de numero de cluster")
plt.legend([line_up, line_down], ['Training Accuracy', 'Testing Accuracy'])
plt.annotate('Overfiting', xy = (1.5, .94), arrowprops = {'facecolor':'gray', 'width': 3, 'shrink': 0.03})
plt.annotate('Optimo', xy = (8, .94), arrowprops = {'facecolor':'gray', 'width': 3, 'shrink': 0.03})
plt.annotate('Underfiting', xy = (16, .94), arrowprops = {'facecolor':'gray', 'width': 3, 'shrink': 0.03})


############
#Regression#
############

gapminder = pd.read_csv("https://assets.datacamp.com/production/repositories/628/datasets/a7e65287ebb197b1267b5042955f27502ec65f31/gm_2008_region.csv")

gapminder = gapminder.drop("Region", axis = 1)

gapminder.head()


# Create arrays for features and target variable
y = gapminder['life'].values
X_fertility = gapminder['fertility'].values

# Print the dimensions of X and y before reshaping
print("Dimensions of y before reshaping: {}".format(y.shape))
print("Dimensions of X before reshaping: {}".format(X.shape))

# Reshape X and y
y = y.reshape(-1, 1)
X_fertility = X_fertility.reshape(-1, 1)

# Print the dimensions of X and y after reshaping
print("Dimensions of y after reshaping: {}".format(y.shape))
print("Dimensions of X after reshaping: {}".format(X.shape))

import seaborn as sns

sns.heatmap(gapminder.corr(), square=True, cmap='RdYlGn')


###########################################
#Ajuste del model y metricas de renimiento#
###########################################

#La precisión en ocasiones no es una métrica de desempeño muy buena, se pueden tener en los datos un desequilibrio de clases.

#Una ejemplo de interpretación erronea sería tener datos con 2 clases No Spam con un 99% de representatividad y Spam con un 1%.
#Nuestro modelo podría cometer el error de clasificar bien los correos no spam dando un 99% de precisión,
#pero el modelo hace un pesimo trabajo para clasificar los correos Spam, por lo que no nos esta ayudando a resolver el problema.

#Esta es una situación muy común en la práctica y requiere una métrica más matizada para evaluar el desempeño de nuestro modelo.

#Dado un clasificador binario, como nuestro ejemplo de correo electrónico no deseado, podemos elaborar una matriz de 2x2
#Llamada matriz de confusión la cual resume el rendimiento predictivo.

#              Predicted: Spam Email   Predicted: Real Email
#Spam Email    True Positive           False Negative
#Real Email    False Positive          True Negative

#¿Como recuperar la precisión de la matriz de confusión

# Accuracy : Tp + Tn / Tp + Tn + Fp + Fn

#Existen otras métricas que pueden calcularse fácilmente a partir de la matriz:
    
    # Precisión (VPP):  Tp / (Tp + Fp) (En el ejemplo del Spam, es el número de Spam correctamente etiquetado)
    
    # Sensibilidad : Tp / (Tp + Fn) (Tasa de aciertos o tasa de verdaderos positivos)
    
    # F1score : 2 * ( (precision * sensibilidad) / (precision + recall) )
    
    
#Alta precisión: no se prevén muchos correos electrónicos reales como spam

#Alta sensibilidad: predice correctamente la mayoría de los correos electrónicos no deseados.

#---
#Aplicando las métricas de evaluación al modelo KNN anteriormente calculado (línea 194)

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

#Matriz de confusión
confusion_matrix(y_test, y_pred)

report_classification = classification_report(y_test, y_pred)
