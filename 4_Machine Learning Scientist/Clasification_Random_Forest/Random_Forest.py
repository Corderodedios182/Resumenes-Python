#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 20:58:30 2020

@author: carlos
"""
import pandas as pd
import seaborn as sns
import plotly.express as px

from sklearn.tree import DecisionTreeClassifier # Import DecisionTreeClassifier
from sklearn.model_selection import train_test_split # Import train_test_split
from sklearn.metrics import accuracy_score # Import accuracy_score
from sklearn.preprocessing import LabelEncoder

#Import dataset
base = pd.read_csv("https://assets.datacamp.com/production/repositories/1796/datasets/0eb6987cb9633e4d6aa6cfd11e00993d2387caa4/wbc.csv")
base.head()
base.shape
list(enumerate(base.keys()))

#Vizualitation
tmp = ['purple' if (radius_mean > 15) & (point_mean > .025) else 'navy' for radius_mean, point_mean in zip(base.radius_mean, base['concave points_mean']) ] #Colores

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
dt = DecisionTreeClassifier(max_depth=2, random_state=1)
dt

# 3 - Fit dt to the training set
dt.fit(X_train, y_train)

# 4 - Predict test set labels
y_pred_tree = dt.predict(X_test)
print(y_pred_tree)

# 5 - Compute test set accuracy
acc = accuracy_score(y_test, y_pred_tree)
print("Test set accuracy: {:.2f}".format(acc))

    #LogisticRegression

from sklearn.linear_model import  LogisticRegression

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
clfs = [logreg, dt]

#
# Review the decision regions of the two classifiers
def plot_labeled_decision_regions(model_1,model_2):
    y_pred_tree
    y_pred_log
    return ""

plot_labeled_decision_regions(X_test, y_test, clfs)















