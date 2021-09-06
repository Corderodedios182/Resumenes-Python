#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 20:58:30 2020

@author: carlos
"""
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.tree import DecisionTreeClassifier # Import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor # Import DecisionTreeClassifier
from sklearn.linear_model import  LogisticRegression 
from sklearn.model_selection import train_test_split # Import train_test_split
from sklearn.metrics import accuracy_score # Import accuracy_score
from sklearn.preprocessing import LabelEncoder

import matplotlib.pyplot as plt
from mlxtend.plotting import plot_decision_regions
import matplotlib.gridspec as gridspec
import itertools
from dtreeviz.trees import *

#Import dataset
base = pd.read_csv("https://assets.datacamp.com/production/repositories/1796/datasets/0eb6987cb9633e4d6aa6cfd11e00993d2387caa4/wbc.csv")
base.head()
base.shape
list(enumerate(base.keys()))

#Grafica de variables
sns.set(style="ticks")
sns.pairplot(base.iloc[:,2:6])

#Vizualisacion de la clasificacion actual
fig = sns.scatterplot(x = base['radius_mean'],
                      y = base['concave points_mean'],
                      hue = base['diagnosis'],
                      style = base['diagnosis']).set_title("Diagnostico tumores")

# -- Entrenando nuestra primera clasificacion --# 

##############################################
# Logistic regression vs classification tree #
##############################################

    #Tree#
#Variables que nos apoyaran a tomar un diagnostico
X = base.loc[:,['radius_mean','concave points_mean']] 
y = range(569)

#1 - Dividiendo el conjunto de datos entrenamiento y test. 80% - 20% 
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2,random_state=1)

#Ingenieria de Variables - Convirtiendo la etiqueta categorica a binaria
lb_make = LabelEncoder()
base['diagnosis'] = lb_make.fit_transform(base['diagnosis'])

#Seleccionando datos entrenamiento
y_train = base.loc[y_train,'diagnosis']
y_test = base.loc[y_test,'diagnosis']

# 2 - Creando una instancia de un arbol
#max_depth = profundidad del arbol
#random_state = Controla la aleatoriedad del estimador
dt = DecisionTreeClassifier(max_depth=2, random_state=5) 
dt

# 3 - Ajuste a los datos de entrenamiento
dt.fit(X_train, y_train)

# 4 - Prediccion del conjutno de prueba
y_pred_tree = dt.predict(X_test)
print(y_pred_tree)

# 5 - Medicion de la presicion
acc = accuracy_score(y_test, y_pred_tree)
print("Test set accuracy: {:.2f}".format(acc))

# 6 - Arbol de desicion 
viz = dtreeviz(dt,
               X_train,
               y_train,
               target_name = 'diagnosis',
               feature_names = ['concave points_mean','radius_mean'],
               class_names = ['B','M'])
              
viz.view()       

    #LogisticRegression

# 2 - Entrenando con LogisticRegression
logreg = LogisticRegression(random_state=1)

# 3 - Ajuste a los datos de entrenamiento
logreg.fit(X_train, y_train)

# 4 - Prediccion al conjunto de Prueba
y_pred_log = logreg.predict(X_test)

# 5 - Midiendo la presicion
acc = accuracy_score(y_test, y_pred_log)
print("Test set accuracy: {:.2f}".format(acc))

# Definiendo en una lista los 2 clasificadores
clfs = [dt, logreg]

#Funcion de apoyo para graficar la region de desicion
def plot_labeled_decision_regions(X_test , y_test, clfs):

    gs = gridspec.GridSpec(2, 2)
    
    fig = plt.figure(figsize=(10,8))
    
    labels = ['Desicio Tree Classfier', 'Logistic Regression']
    
    for clfs, lab, grd in zip([dt, logreg], labels, itertools.product([0, 1], repeat=2)):
    
        clfs.fit(np.array(X_test), np.array(y_test))
        
        ax = plt.subplot(gs[grd[0], grd[1]])
        
        fig = plot_decision_regions(X = np.array(X_test),
                                    y = np.array(y_test),
                                    clf=clfs,
                                    legend=2,
                                    zoom_factor = 20)
        
        plt.title(lab)
    
    plt.show()

# Revisando las regiones de desicion de los clasificadores
plot_labeled_decision_regions(X_train, y_train, clfs)

# ¿Como sabe un arbol que funcion y que punto dividir? 
# Lo hace maximizando la ganancia de informacion (IG)

#Criterios de entropia y gini

# Instantiate dt_entropy, set 'entropy' as the information criterion
dt_entropy = DecisionTreeClassifier(max_depth=8, criterion='entropy', random_state=1)

# Fit dt_entropy to the training set
dt_entropy.fit(X_train, y_train)

#Midiendo el Error Generalizado de un Modelo
#Recordando que el Error Generalizado busca analizar la capacidad de aprender de nuevos datos
#Decimos que el modelo de machine learning ha aprendido «de memoria» cuando:

#el error de entrenamiento es bajo 
#el error de generalización es alto

#Aprendio bien de los datos de entrenamiento pero no Generaliza bien los datos de Test

#Error Generalizado
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error as MSE
from sklearn.model_selection import cross_val_score

SEED = 1

X = base.loc[:,['radius_mean','concave points_mean']] 
y = range(569)

#1 - Dividiendo el conjunto de datos entrenamiento y test. 80% - 20% 
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2,random_state=1)

#Ingenieria de Variables - Convirtiendo la etiqueta categorica a binaria
lb_make = LabelEncoder()
base['diagnosis'] = lb_make.fit_transform(base['diagnosis'])

#Seleccionando datos entrenamiento y test
y_train = base.loc[y_train,'diagnosis']
y_test = base.loc[y_test,'diagnosis']

# 2 - Instantiate a DecisionTreeRegressor dt
dt = DecisionTreeRegressor(max_depth=4, min_samples_leaf=.26, random_state=SEED)
dt

# 3 - Ajuste a los datos de entrenamiento 
dt.fit(X_train, y_train)

# 4.1 - Prediccion del conjunto de entrenamiento y test
y_predict_train = dt.predict(X_train)

# MSE del conjunto de entrenamiento
print('Train MSE: {:.2f}'.format(MSE(y_train, y_predict_train)))

# 4.2 - Predicciones con el conjunto de Testeo
y_predict_test = dt.predict(X_test)

# MSE del conjunto de testeo
print('Test MSE: {:.2f}'.format(MSE(y_test, y_predict_test)))

# 5 - Cros Validation
# Evaluando el MSE con un CV de 10
MSE_CV = - cross_val_score(dt, X_train, y_train, cv= 10,
                           scoring='neg_mean_squared_error',
                           n_jobs = -1)

print('CV MSE: {:.2f}'.format(MSE_CV.mean()))

#Viendo los 3 MSE podemos concluir que tienen un MSE similar por lo que el modelo parece Generalizar bien con los diferentes set de datos

##Metodo de Ensamble
# Import functions to compute accuracy and split data
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Import models, including VotingClassifier meta-model
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.ensemble import VotingClassifier

# Set seed for reproducibility
SEED=1

# Instantiate lr
lr = LogisticRegression(random_state=SEED)

# Instantiate knn
knn = KNN(n_neighbors=27)

# Instantiate dt
dt = DecisionTreeClassifier(min_samples_leaf=0.13, random_state=SEED)

# Define the list classifiers
classifiers = [('Logistic Regression', lr), ('K Nearest Neighbours', knn), ('Classification Tree', dt)]

# Iterate over the pre-defined list of classifiers
for clf_name, clf in classifiers:    
  
    # Fit clf to the training set
    clf.fit(X_train, y_train)    
  
    # Predict y_pred
    y_pred = clf.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
  
    # Evaluate clf's accuracy on the test set
    print('{:s} : {:.3f}'.format(clf_name, accuracy))


# Import VotingClassifier from sklearn.ensemble
from sklearn.ensemble import VotingClassifier

# Instantiate a VotingClassifier vc 
vc = VotingClassifier(estimators=classifiers)     

# Fit vc to the training set
vc.fit(X_train, y_train)   

# Evaluate the test set predictions
y_pred = vc.predict(X_test)

# Calculate accuracy score
accuracy = accuracy_score(y_test, y_pred)
print('Voting Classifier: {:.3f}'.format(accuracy))


