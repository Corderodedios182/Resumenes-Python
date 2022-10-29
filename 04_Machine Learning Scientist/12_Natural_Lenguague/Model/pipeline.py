# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 12:20:51 2022

@author: cflorelu
"""

from settings import *
from importData import * 
from preprocessing import *
from exploratoryData import *
from dataModeling import *
from trainModel import *
from reporting import *

from text_utils import *

#-- importData --#

datos = read_data(ruta_feedback)

#-- preprocessing --#

datos = reordering_data(datos_a_corregir = datos)

datos = vectorizing_data(datos_a_procesar = datos,
                         model_w2v = model_w2v,
                         pdt = ProcesadorDeTexto())

#-- exploratoryData --#
exploratoryDataframe(datos)

#-- dataModeling --#
datos_model = datos.iloc[:,[5,7,8,9,6]]
X, y , Qids = obtener_CEQs(datos_model)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=2)

#-- ModeloXGboostRegresor --#
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import mean_squared_error as MSE
from xgboost import XGBRegressor

kfold = KFold(n_splits=5, shuffle=True, random_state=2)

def cross_val(model):
    scores = cross_val_score(model, X_train, y_train, scoring='neg_root_mean_squared_error', cv=kfold)
    rmse = (-scores.mean())
    return rmse

cross_val(XGBRegressor(missing=-999.0))

X_train_2, X_test_2, y_train_2, y_test_2 = train_test_split(X_train, y_train, random_state=2)

def n_estimators(model):

    eval_set = [(X_test_2, y_test_2)]
    eval_metric="rmse"
    model.fit(X_train_2, y_train_2,
              eval_metric=eval_metric,
              eval_set=eval_set,
              early_stopping_rounds=100)

    y_pred = model.predict(X_test_2)

    rmse = MSE(y_test_2, y_pred)**0.5

    return rmse  

n_estimators(XGBRegressor(n_estimators=5000, missing=-999.0)) #Mejor n_estimator = 9

def grid_search(params, reg=XGBRegressor(missing=-999.0)):

    grid_reg = GridSearchCV(reg, params, scoring='neg_mean_squared_error', cv=kfold)
    grid_reg.fit(X_train, y_train)

    best_params = grid_reg.best_params_

    print("Best params:", best_params)

    best_score = np.sqrt(-grid_reg.best_score_)

    print("Best score:", best_score)
    
grid_search(params={'max_depth':[1, 2, 3, 4, 6, 7, 8], #max_depth = 3
                    'n_estimators':[9]}) 

grid_search(params={'max_depth':[1, 2, 3],
                    'min_child_weight':[1,2,3,4,5], #min_child_weight = 1
                    'n_estimators':[9]}) 

grid_search(params={'max_depth':[1],
                    'min_child_weight':[1,2],
                    'subsample':[0.5, 0.6, 0.7, 0.8, 0.9], #sumbsample = .9
                    'n_estimators':[8,9]})

grid_search(params={'max_depth':[1],
                    'min_child_weight':[1, 2, 3], #min_child_weight = 3
                    'subsample':[0.7, 0.8, 0.9],
                    'colsample_bytree':[0.5, 0.6, 0.7, 0.8, 0.9, 1], #colsample = .5
                    'n_estimators':[9]})

grid_search(params={'max_depth':[1],
                    'min_child_weight':[3],
                    'subsample':[.8],
                    'colsample_bytree':[0.5],
                    'colsample_bylevel':[0.6, 0.7, 0.8, 0.9, 1],
                    'colsample_bynode':[0.6, 0.7, 0.8, 0.9, 1],
                    'n_estimators':[9]})

model = XGBRegressor(max_depth = 1,
                     min_child_weight = 3,
                     subsample=0.8,
                     n_estimators = 9,
                     colsample_bytree=0.5,
                     gamma=2,
                     missing=-999.0)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

rmse = MSE(y_pred, y_test)**0.5
rmse

pd.DataFrame(y_pred).describe()

#ndcg
y_pred
y_test

#Incluir info con más evaluación
#XboostRanker
#Muestreo representativo -> 
#

#-- ModeloXGbosstRanker --#
from sklearn.metrics import average_precision_score, ndcg_score
from sklearn.model_selection import GroupShuffleSplit
import xgboost

model = xgboost.XGBRanker(objective='rank:ndcg', 
                          n_estimators=9,
                          subsample=.9,
                          reg_lambda = 0.1)

model.fit(
    X_train,
    y_train,
    group = Qids.iloc[y_train.index,:],
    eval_metric='ndcg',
    eval_set=[(X_test, y_test)],
    eval_group=[list(query_list_test)],
    verbose =True
)

#-- reporting-- #
