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

#import os
#os.listdir()
#os.chdir("'C:\\Users\\Maste\\Documents\\1_Github\\Resumenes-Python\\4_Machine Learning Scientist'")

import plot_classifier as plt_cls
import numpy as np

from sklearn.linear_model import LogisticRegression
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
