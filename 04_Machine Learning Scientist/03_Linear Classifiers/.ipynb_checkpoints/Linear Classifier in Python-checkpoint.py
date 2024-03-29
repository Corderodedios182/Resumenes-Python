# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 10:29:03 2021

@author: Maste
"""

# Trabajando con diferentes clasificadores lineales, veremos las regiones de desicion que pueden generar.

#Definiciones utiles: 

# Clasificación: aprender a predecir categorías

# Límite de decisión: la superficie que separa diferentes clases predichas

# Clasificador lineal: un clasificador que aprende límites de decisión lineal
#   regresión logística, SVM lineal

# Separable linealmente: un conjunto de datos se puede explicar perfectamente mediante un clasificador lineal

import os
os.listdir()
os.chdir("C:\\Users\\Maste\\Documents\\1_Github\\Resumenes-Python\\4_Machine Learning Scientist") #C:\\Users\\crf005r\\Documents\\3_GitHub\\Resumenes-Python\\4_Machine Learning Scientist

import matplotlib.pyplot as plt 
import plot_classifier as plt_cls
import numpy as np

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.neighbors import KNeighborsClassifier

X = [[11.45,  2.4 ],[13.62,  4.95],[13.88,  1.89],[12.42,  2.55],[12.81,  2.31],[12.58,  1.29],[13.83,  1.57],[13.07,  1.5 ],[12.7 ,  3.55],[13.77,  1.9 ],
       [12.84,  2.96],[12.37,  1.63],[13.51,  1.8 ],[13.87,  1.9 ],[12.08,  1.39],[13.58,  1.66],[13.08,  3.9 ],[11.79,  2.13],[12.45,  3.03],[13.68,  1.83],
       [13.52,  3.17],[13.5 ,  3.12],[12.87,  4.61],[14.02,  1.68],[12.29,  3.17],[12.08,  1.13],[12.7 ,  3.87],[11.03,  1.51],[13.32,  3.24],[14.13,  4.1 ],
       [13.49,  1.66],[11.84,  2.89],[13.05,  2.05],[12.72,  1.81],[12.82,  3.37],[13.4 ,  4.6 ],[14.22,  3.99],[13.72,  1.43],[12.93,  2.81],[11.64,  2.06],
       [12.29,  1.61],[11.65,  1.67],[13.28,  1.64],[12.93,  3.8 ],[13.86,  1.35],[11.82,  1.72],[12.37,  1.17],[12.42,  1.61],[13.9 ,  1.68],[14.16,  2.51]]

X = np.array(X)

y = [True,  True, False,  True,  True,  True, False, False,  True, False,  True,  True, False, False,  True, False,  True,  True,
     True, False,  True,  True,  True, False,  True,  True,  True, True,  True,  True,  True,  True, False,  True,  True,  True,
     False, False,  True,  True,  True,  True, False, False, False, True,  True,  True, False,  True]

y = np.array(y)

# Definiendo clasificadores
classifiers = [LogisticRegression(), LinearSVC(), SVC(), KNeighborsClassifier()]

# Entrenamiento de clasificadores
for c in classifiers:
    c.fit(X, y)

# Grafica clasificadores
# Visualización de límites de desición

plt_cls.plot_4_classifiers(X, y, classifiers)

####################
#Funcion de Perdida#
####################

#Veamos el marco conceptual detrás de la regresión logística y las SVM.
#Esto permitirá profundizar en el funcionamiento interno de estos modelos.

#Los coeficientes y parametros juegan un papel importante al crear la región de desición
#¿Como genera la clasificacion Logistic Regression?
#Revisamos si es positiva (predicen la clase) o negativa
#salida_modelo = coefficients * geatures + intercept

#Veamos los parametros que genera el siguiente modelo
lr = LogisticRegression()
lr.fit(X,y)

lr.predict(X)[10] #Salida final de el metodo predict
lr.predict(X)[2]

#¿Como genera la clasificación internamente, por medio de los coeficientes e interceptos
#Si es positivo lo clasifica como 1
lr.coef_ @ X[10] + lr.intercept_ #El @ es producto escalar
#Si es negativo lo clasifica como 0
lr.coef_ @ X[2] + lr.intercept_ #El @ es producto escalar

plt_cls.plot_classifier(X,y,lr)
num_err = np.sum(y != lr.predict(X))
print("Numero de errores:", num_err)

#Ajustando los coeficientes veamos si incrementa la presición o disminuye
lr.coef_ = np.array([[-2,1]])
lr.intercept_ = np.array([24])

plt_cls.plot_classifier(X,y,lr)
num_err = np.sum(y != lr.predict(X))
print("Numero de errores:", num_err)

#---------------------------------------------------------------------------#
#Muchos algoritmos de aprendizaje automático implican minimizar una funcion de pérdida.

#Nota; No confundir la función de puntuación model.score() con las funciones de perdida.
#La pérdida se usa para ajustar el modelo en los datos, y model.score() se usa para ver qué tan bien los estamos haciendo.

#Ejemplos de funciones perdida para algunos algoritmos:
    
#En Regresión Líneal (LinearRegression) tenemos : Mínimos Cuadrados  

#Clustering : El número de errores podría ser una buena función de perdida. (0-1)

#Regresión logística :
    
#SVM : 

#Estas funciones de perdida son el objetivo a minimizar para tener un mejor rendimiento en los modelos

#El error cuadrado no es apropiado para problemas de clasificación ya que los valores de salida son categoricos, lo normal es pensar en la cantidad
#de errores que se han cometido

#Minimizando funciones con python

from scipy.optimize import minimize

minimize(np.square,0).x #Valor minimo de la función x = 0

#Veamos como minimizar el error al cuadrado de la regresión lineal.
def my_loss(w):
    s = 0
    for i in range(y.size):
        # Obtenga los valores objetivo verdaderos y predichos, por ejemplo, 'i'
        y_i_true = y[i]
        y_i_pred = w @ X[i] # @ Es el producto escalar
        s = s + (y_i_true - y_i_pred)**2 #Error cuadratico
    return s

#Minimizando la funcion de perdidad error cuadratico
w_fit = minimize(my_loss, X[0]).x
#Coeficientes de la minimizacion función de perdida
print(w_fit)

# Coeficientes sin la minimizacion
lr = LinearRegression(fit_intercept=False).fit(X,y)
print(lr.coef_)
print(lr.intercept_)

#Diagramas de funciones de perdida
# Funciones matemáticas para pérdidas logísticas y de bisagra
def log_loss(raw_model_output):
   return np.log(1+np.exp(-raw_model_output))

def hinge_loss(raw_model_output):
   return np.maximum(0,1-raw_model_output)

# Crea una cuadrícula de valores y traza
grid = np.linspace(-2,2,1000)
plt.plot(grid, log_loss(grid), label='logistic')
plt.plot(grid, hinge_loss(grid), label='hinge')
plt.legend()
plt.show()

# La pérdida logística, resumida en ejemplos de formación
def my_loss(w):
    s = 0
    for i in range(y.size):
        raw_model_output = w@X[i]
        s = s + log_loss(raw_model_output * y[i])
    return s

# Devuelve la w que hace que my_loss (w) sea la más pequeña
w_fit = minimize(my_loss, X[0]).x
print(w_fit)

# Comparar con LogisticRegression de scikit-learn
lr = LogisticRegression(fit_intercept=False, C=1000000).fit(X,y)
print(lr.coef_)

#La regresión logística solo minimiza la función de pérdida que hemos estado analizando.

#---------------------------------------------------------------------------#
#Regresion Logistica#

#¿Qué es la regularización en machine learning?
#En muchas técnicas de aprendizaje automático, el aprendizaje consiste en encontrar los coeficientes que minimizan una función de coste.
#La regularización consiste en añadir una penalización a la función de coste. 
#Esta penalización produce modelos más simples que generalizan mejor.

#La técnica de regularización puede ser empleada para corregir el sobreajuste.
#Esta técnica puede emplearse en un conjunto amplio de técnicas de minería de datos como regresión linear, regresión logística, SVM, etc.
#La regularización consiste en reducir la importancia de los parámetros θj que aparecen en la función de coste.
#Este efecto se consigue mediante la inclusión de los parámetros θj en la función de coste J(θ).

#Finalmente podremos variar los parámetros de regularización para entender como la regularización soluciona el problema de Overfitting.
#Note los cambios en los limites de decisión al variar lamda. 

#Para un valor de lamda muy pequeño, el clasificador predice casi exactamente los datos de entrenamiento,
#creándose una frontera de decisión compleja, presentándose así Overtiffitng, y la predicción para un nuevo dato no resulta ser correcta,



















