# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 10:29:03 2021

@author: Maste
"""

#En este capítulo, aprenderá los conceptos básicos de la aplicación de regresión logística y máquinas de vectores de soporte (SVM) a problemas de clasificación.

#Utilizará la biblioteca scikit-learn para ajustar los modelos de clasificación a datos reales.

import sklearn.datasets

newsgroup = sklearn.datasets.fetch_20newsgroups_vectorized()
X, y = newsgroup.data, newsgroup.target 
X.shape
y.shape

import pandas as pd
X_dataframe = pd.DataFrame(X.todense())

#Prediccion 
from sklearn.neighbors import KNeighborsClassifier

#Instanciando 2 modelos diferentes
knn_1 = KNeighborsClassifier(n_neighbors=1)
knn_2 = KNeighborsClassifier(n_neighbors=2)

#Entrenando el modelo con todos los datos
knn_1.fit(X,y)

y_pred = knn_1.predict(X)

#Evaluacion del modelo, erronea ya que debemos ver la presicion con datos invisibles.
knn_1.score(X,y)

#Separando datos de entrenamiento y test
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X,y)

#Entrenando 2 modelos
knn_1.fit(X_train,y_train)
knn_2.fit(X_train,y_train)

# Predict on the test features, print the results
pred_1 = knn_1.predict(X_test)
pred_2 = knn_2.predict(X_test)

knn_1.score(X_test, y_test)
knn_2.score(X_test, y_test)

from sklearn.metrics import accuracy_score 
# Este accuracy es lo mismo que knn.score
accuracy_score(pred_1, y_test)
accuracy_score(pred_2, y_test)
