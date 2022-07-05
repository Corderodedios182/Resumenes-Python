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
#from dtreeviz.trees import *

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
#viz = dtreeviz(dt,
#               X_train,
#               y_train,
#               target_name = 'diagnosis',
#               feature_names = ['concave points_mean','radius_mean'],
#               class_names = ['B','M'])
              
#viz.view()       

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

#Bagging and Random Forests
#Bagging es un método de conjunto que implica entrenar el mismo algoritmo muchas veces usando diferentes subconjuntos muestreados de los datos de entrenamiento.
#Cómo se puede utilizar el Bagging para crear un conjunto de árbol.
#También aprenderá cómo el algoritmo de bosques aleatorios puede conducir a una mayor diversidad de conjuntos a través de la aleatorización
#al nivel de cada división en los árboles que forman el conjunto.

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier

#Define the bagging classifier
dt = DecisionTreeClassifier(random_state=1)
bc = BaggingClassifier(base_estimator=dt, n_estimators=50, random_state=1)

#Evaluate Bagging performance

# Fit bc to the training set
bc.fit(X_train, y_train)

# Predict test set labels
y_pred = bc.predict(X_test)

# Evaluate acc_test
acc_test = accuracy_score(y_test, y_pred)
print('Test set accuracy of bc: {:.2f}'.format(acc_test)) 

#- Out of Bag Evaluation

# Import DecisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier

# Import BaggingClassifier
from sklearn.ensemble import BaggingClassifier

# Instantiate dt
dt = DecisionTreeClassifier(min_samples_leaf=8, random_state=1)

# Instantiate bc
bc = BaggingClassifier(base_estimator=dt, 
            n_estimators=50,
            oob_score=True,
            random_state=1)

# Fit bc to the training set 
bc.fit(X_train, y_train)

# Predict test set labels
y_pred = bc.predict(X_test)

# Evaluate test set accuracy
acc_test = accuracy_score(y_pred, y_test)

# Evaluate OOB accuracy
acc_oob = bc.oob_score_

# Print acc_test and acc_oob
print('Test set accuracy: {:.3f}, OOB accuracy: {:.3f}'.format(acc_test, acc_oob))

# - Random Forest

X = base.drop(['id','diagnosis','Unnamed: 32'], axis = 1)
y = range(569)

#1 - Dividiendo el conjunto de datos entrenamiento y test. 80% - 20% 
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2,random_state=1)

#Ingenieria de Variables - Convirtiendo la etiqueta categorica a binaria
lb_make = LabelEncoder()
base['diagnosis'] = lb_make.fit_transform(base['diagnosis'])

#Seleccionando datos entrenamiento
y_train = base.loc[y_train,'diagnosis']
y_test = base.loc[y_test,'diagnosis']

# Import RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor

# Instantiate rf
rf = RandomForestRegressor(n_estimators=25,
            random_state=2)
            
# Fit rf to the training set    
rf.fit(X_train, y_train) 

# Import mean_squared_error as MSE
from sklearn.metrics import mean_squared_error as MSE

# Predict the test set labels
y_pred = rf.predict(X_test)

# Evaluate the test set RMSE
rmse_test = MSE(y_test, y_pred)**(1/2)

# Print rmse_test
print('Test set RMSE of rf: {:.2f}'.format(rmse_test))

# Create a pd.Series of features importances
importances = pd.Series(data=rf.feature_importances_,
                        index= X_train.columns)

# Sort importances
importances_sorted = importances.sort_values()

# Draw a horizontal barplot of importances_sorted
importances_sorted.plot(kind='barh', color='lightgreen')
plt.title('Features Importances')
plt.show()

###Boosting##

#Boosting se refiere a un método de conjunto en el que varios modelos se entrenan secuencialmente y cada modelo aprende de los errores de sus predecesores.
#Se presentarán los dos métodos de refuerzo de AdaBoost y Gradient Boosting.

# Import DecisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier

# Import AdaBoostClassifier
from sklearn.ensemble import AdaBoostClassifier

# Instantiate dt
dt = DecisionTreeClassifier(max_depth=2, random_state=1)

# Instantiate ada
ada = AdaBoostClassifier(base_estimator=dt, n_estimators=180, random_state=1)

# Fit ada to the training set
ada.fit(X_train, y_train)

# Compute the probabilities of obtaining the positive class
y_pred_proba = ada.predict_proba(X_test)[:,1]

# Import roc_auc_score
from sklearn.metrics import roc_auc_score

# Evaluate test-set roc_auc_score
ada_roc_auc = roc_auc_score(y_test, y_pred_proba)

# Print roc_auc_score
print('ROC AUC score: {:.2f}'.format(ada_roc_auc))

####Gradient Boosting

# Import GradientBoostingRegressor
from sklearn.ensemble import GradientBoostingRegressor

# Instantiate gb
gb = GradientBoostingRegressor(n_estimators=200, 
            max_depth=4,
            random_state=2)

# Fit gb to the training set
gb.fit(X_train, y_train)

# Predict test set labels
y_pred = gb.predict(X_test)

# Import mean_squared_error as MSE
from sklearn.metrics import mean_squared_error as MSE

# Compute MSE
mse_test = MSE(y_test,y_pred)

# Compute RMSE
rmse_test = mse_test**(1/2)

# Print RMSE
print('Test set RMSE of gb: {:.3f}'.format(rmse_test))


#####Stochastic Gradient Boosting (SGB)

# Import GradientBoostingRegressor
from sklearn.ensemble import GradientBoostingRegressor

# Instantiate sgbr
sgbr = GradientBoostingRegressor(max_depth=4, 
            subsample=.9,
            max_features=.75,
            n_estimators=200,                                
            random_state=2)

# Fit sgbr to the training set
sgbr.fit(X_train,y_train)

# Predict test set labels
y_pred = sgbr.predict(X_test)

# Import mean_squared_error as MSE
from sklearn.metrics import mean_squared_error as MSE

# Compute test set MSE
mse_test = MSE(y_test, y_pred)

# Compute test set RMSE
rmse_test = mse_test**(1/2)

# Print rmse_test
print('Test set RMSE of sgbr: {:.3f}'.format(rmse_test))

#####Inpecting the hyperparameters of a CART in sklearn

# Import DecisionTreeClassifier 
from sklearn.tree import DecisionTreeClassifier

# Set seed to 1 for reproducibility 
SEED = 1

# Instantiate a DecisionTreeClassifier 'dt'
dt = DecisionTreeClassifier(random_state=SEED)

dt.get_params()

##Aproaches to hyperparameter tuning 

#Grid Search

# Import GridSearchCV
from sklearn.model_selection import GridSearchCV

# Define the grid of hyperparameters 'params_dt'
params_dt = {'max_depth': [3, 4,5, 6],
             'min_samples_leaf': [0.04, 0.06, 0.08],
             'max_features': [0.2, 0.4,0.6, 0.8]}

# Instantiate a 10-fold CV grid search object 'grid_dt'
grid_dt = GridSearchCV(estimator=dt,
                       param_grid=params_dt,
                       scoring='accuracy',
                       cv=10,
                       n_jobs=-1)

# Fit 'grid_dt' to the training data
grid_dt.fit(X_train, y_train)

# Extract best hyperparameters from 'grid_dt'
best_hyperparams = grid_dt.best_params_

print('Best hyerparameters:\n', best_hyperparams)

# Extract best CV score from 'grid_dt'
best_CV_score = grid_dt.best_score_

'Best CV accuracy {}'.format(best_CV_score)

# Extract best model from 'grid_dt'
best_model = grid_dt.best_estimator_

# Evaluate test set accuracy
test_acc = best_model.score(X_test,y_test)

# Print test set accuracy
print("Test set accuracy of best model: {:.3f}".format(test_acc))

## - Hyperparameters Grid

# Define the dictionary 'params_rf'
params_rf = {'n_estimators': [100, 350, 500],
             'max_features': ['log2','auto','sqrt'],
             'min_samples_leaf': [2,10,30]}

# Import GridSearchCV
from sklearn.model_selection import  GridSearchCV

# Instantiate grid_rf
grid_rf = GridSearchCV(estimator=rf,
                       param_grid=params_rf,
                       scoring='neg_mean_squared_error',
                       cv=3,
                       verbose=1,
                       n_jobs=-1)

# Import mean_squared_error from sklearn.metrics as MSE 
from sklearn.metrics import mean_squared_error as MSE

grid_rf.fit(X_train, y_train)

# Extract the best estimator
best_model = grid_rf.best_estimator_

# Predict test set labels
y_pred = best_model.predict(X_test)

# Compute rmse_test
rmse_test = MSE(y_test, y_pred)**(1/2)

# Print rmse_test
print('Test RMSE of best model: {:.3f}'.format(rmse_test)) 

#Prueba para conflicto