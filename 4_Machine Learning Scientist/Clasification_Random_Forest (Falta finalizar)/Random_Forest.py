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

sns.set(style="ticks")
sns.pairplot(base.iloc[:,2:6])

#Vizualitation
fig = sns.scatterplot(x = base['radius_mean'],
                  y = base['concave points_mean'],
                  hue = base['diagnosis'],
                  style = base['diagnosis']).set_title("Diagnostico tumores")

# -- Train your first classification --# 

##############################################
# Logistic regression vs classification tree #
##############################################

    #Tree#

# Split dataset into 80% train, 20% test
X = base.loc[:,['radius_mean','concave points_mean']] #Variables que nos apoyaran a tomar un diagnostico
y = range(569)

#1 - Dividiendo el conjunto de datos entrenamiento y test.
X_train, X_test, y_train, y_test= train_test_split(X, y,test_size=0.2,random_state=1)

lb_make = LabelEncoder()
base['diagnosis'] = lb_make.fit_transform(base['diagnosis']) #Convertir etiqueta cateorica a binaria

#Seleccionando datos entrenamiento
y_train = base.loc[y_train,'diagnosis']
y_test = base.loc[y_test,'diagnosis']

# 2 - Train your first classification tree
dt = DecisionTreeClassifier(max_depth=2, random_state=5)
dt

# 3 - Fit dt to the training set
dt.fit(X_train, y_train)

# 4 - Predict test set labels
y_pred_tree = dt.predict(X_test)
print(y_pred_tree)

# 5 - Compute test set accuracy
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

# 2 - Train your first classification LogisticRegression
logreg = LogisticRegression(random_state=1)

# 3 - Fit logreg to the training set
logreg.fit(X_train, y_train)

# 4 - Predict test set labels
y_pred_log = logreg.predict(X_test)

# 5 - Compute test set accuracy
acc = accuracy_score(y_test, y_pred_log)
print("Test set accuracy: {:.2f}".format(acc))

# Define a list called clfs containing the two classifiers logreg and dt
clfs = [dt, logreg]

#Function graph regions models
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

# Review the decision regions of the two classifiers
plot_labeled_decision_regions(X_train, y_train, clfs)

#Criterios de entropia y gini

# Instantiate dt_entropy, set 'entropy' as the information criterion
dt_entropy = DecisionTreeClassifier(max_depth=8, criterion='entropy', random_state=1)

# Fit dt_entropy to the training set
dt_entropy.fit(X_train, y_train)


