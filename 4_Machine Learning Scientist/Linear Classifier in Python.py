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

#Prediccion 
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=1)

knn.fit(X,y)

y_pred = knn.predict(X)

#Evaluacion del modelo, erronea ya que debemos ver la presicion con datos invisibles.
knn.score(X,y)

#Separando datos de entrenamiento y test
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X,y)

knn.fit(X_train,y_train)

knn.score(X_test, y_test)





