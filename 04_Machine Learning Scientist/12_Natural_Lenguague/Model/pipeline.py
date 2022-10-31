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
datos_test = read_data_test()

#-- preprocessing --#

datos = reordering_data(datos_a_corregir = datos)

datos = vectorizing_data(datos_a_procesar = datos,
                         model_w2v = model_w2v,
                         pdt = ProcesadorDeTexto()).reset_index()

datos["index"] = datos.index

#-- exploratoryData --#
exploratoryDataframe(datos)

#-- dataModeling --#
datos_model = datos.iloc[:,[5,7,8,9,6]]

#-- ModeloXGboostRegresor --#
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import mean_squared_error as MSE
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import ndcg_score

x = []
y = []

X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=2)

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

n_estimators(XGBRegressor(n_estimators=5000, missing=-999.0)) #Mejor n_estimator = 10

def grid_search(params, reg=XGBRegressor(missing=-999.0)):

    grid_reg = GridSearchCV(reg, params, scoring='neg_mean_squared_error', cv=kfold)
    grid_reg.fit(X_train, y_train)

    best_params = grid_reg.best_params_

    print("Best params:", best_params)

    best_score = np.sqrt(-grid_reg.best_score_)

    print("Best score:", best_score)
    
grid_search(params={'max_depth':[1, 2, 3, 4, 6, 7, 8], #max_depth = 8
                    'n_estimators':[10]}) 

grid_search(params={'max_depth':[8],
                    'min_child_weight':[1,2,3,4,5], #min_child_weight = 2
                    'n_estimators':[10]}) 

grid_search(params={'max_depth':[8],
                    'min_child_weight':[1,2],
                    'subsample':[0.5, 0.6, 0.7, 0.8, 0.9], #sumbsample = .9
                    'n_estimators':[8,9]})

grid_search(params={'max_depth':[8],
                    'min_child_weight':[1, 2], #min_child_weight = 2
                    'subsample':[0.9],
                    'colsample_bytree':[0.5, 0.6, 0.7, 0.8, 0.9, 1], #colsample = 1
                    'n_estimators':[10]})

grid_search(params={'max_depth':[8],
                    'min_child_weight':[2],
                    'subsample':[.9],
                    'colsample_bytree':[1],
                    'colsample_bylevel':[0.6, 0.7, 0.8, 0.9, 1],
                    'colsample_bynode':[0.6, 0.7, 0.8, 0.9, 1],
                    'n_estimators':[10]})

#Best model
model = XGBRegressor(max_depth = 8,
                     min_child_weight = 2,
                     subsample = 0.9,
                     n_estimators = 10,
                     colsample_bytree = 1,
                     gamma = 2,
                     missing = -999.0)

model.fit(X_train, y_train)

# --Reporting-- #
#Datos de entrenamiento
y_pred_train = model.predict(X_train)

y_train = pd.DataFrame(y_train)
y_train = y_train.reset_index()

results_train = pd.concat([y_train,
                           pd.DataFrame(y_pred_train, columns = ["y_pred_train"])], axis = 1)

results_train["y_pred_train"] = round(results_train["y_pred_train"])

rmse = MSE(results_train["y_pred_train"], results_train["QID"])**0.5 ; rmse

ndcg_score(np.asarray([results_train["QID"]]),
           np.asarray([results_train["y_pred_train"]]))

#Datos de test
y_pred_test = model.predict(X_test)

y_test = pd.DataFrame(y_test)
y_test = y_test.reset_index()

results = pd.concat([y_test,
                     pd.DataFrame(y_pred_test, columns = ["y_pred_test"])], axis = 1)

results["y_pred_test"] = round(results["y_pred_test"])

rmse = MSE(results["y_pred_test"], results["QID"])**0.5 ; rmse

ndcg_score(np.asarray([results["QID"]]),
           np.asarray([results["y_pred_test"]]))

results["diferencia_qid"] = results["QID"] - results["y_pred_test"]

results["y_pred_test"] = results["y_pred_test"].astype(int)

diccionario = datos.loc[:,["QID","TEXTO_COMPARACION"]].drop_duplicates()

results = pd.merge(
                   results,
                   diccionario,
                   left_on = 'y_pred_test',
                   right_on = 'QID',
                   how = 'inner')

results = pd.merge(
                   datos.loc[:,["index","QID","TEXTO_COMPARACION","D_EVENTO","SIMILITUD","EVALUACION","rank"]],
                   results,
                   on = 'index',
                   how = 'right')

# Características del conjunto de datos

x_entrna, y_entrna, x_valida, y_valida, x_prueba, y_prueba = split_data(datos_a_dividir = datos,
                                                                        p_explr_prueba = .90,
                                                                        p_entrn_valida = .89,
                                                                        )

# Entrenamiento
## Listas con las características, etiquetas y grupos utilizadas en el entrenamiento del modelo
feats_entrna, labels_entrna, qids_entrna = \
    obtener_CEQs(
        X=x_entrna,
        y=y_entrna,
        noms_cols_caracts=noms_cols_caracts
    )
## Listas con las características, etiquetas y grupos utilizadas en la validación del entrenamiento del modelo
feats_valida, labels_valida, qids_valida = \
    obtener_CEQs(
        X=x_valida,
        y=y_valida,
        noms_cols_caracts=noms_cols_caracts,
    )
## Listas con las características, etiquetas y grupos utilizadas en la prueba del modelo
feats_prueba, labels_prueba, qids_prueba = \
    obtener_CEQs(
        X=x_prueba,
        y=y_prueba,
        noms_cols_caracts=noms_cols_caracts,
    )

# -- LGBMRanker -- #

import numpy as np
import pandas as pd
import lightgbm

import lightgbm as lgb
ranker = lgb.LGBMRanker()

print("X_tr:", feats_entrna.shape)
print("y_tr:", labels_entrna.shape)
print("group_tr:", qids_entrna.shape)

print("X_t:", feats_prueba.shape)
print("y_t", labels_prueba.shape)
print("group_t", qids_prueba.shape)


ranker.fit(feats_entrna,
           labels_entrna,
           group = qids_entrna,
           eval_set=[(feats_prueba, labels_prueba)],
           eval_group=[qids_prueba],
           eval_at=[1],
           verbose=True,
           callbacks=[lgb.reset_parameter(learning_rate=lambda x: 0.95 ** x * 0.1)]
           )

model = lightgbm.LGBMRanker(objective="lambdarank",
                            metric="ndcg")

model.fit(X = feats_entrna,
          y = labels_entrna,
          group = qids_entrna,
          eval_set=[(feats_valida, labels_valida)],
          eval_group=[qids_valida],
          eval_at=1,
          verbose=1)

#-- ModeloXGbosstRanker --#
from sklearn.metrics import average_precision_score, ndcg_score
from sklearn.model_selection import GroupShuffleSplit
import xgboost

params = {'objective': 'rank:ndcg',
          'eval_metric': [
                'map',
                'ndcg',
                'ndcg@5',
                'ndcg@10',
                'rmse',
                'auc']
    }

model_l2r = xgboost.XGBRanker(**params)

model_l2r.fit(X = feats_entrna,
              y = labels_entrna,
              qid = qids_entrna,
              eval_set = \
                  [
                      (feats_entrna, labels_entrna), 
                      (feats_valida, labels_valida)
                      ],
                  eval_qid = \
                      [
                          qids_entrna,
                          qids_valida,
                          ],
                      verbose = False,
                      )

evals_result = model_l2r.evals_result()

print('Los 5 últimos:')
print()
print(f"MAPs (entrenamiento): {evals_result['validation_0']['map'][-5:]}")
print(f"NDCGs (entrenamiento): {evals_result['validation_0']['ndcg'][-5:]}")
print(f"NDCG@5s (entrenamiento): {evals_result['validation_0']['ndcg@5'][-5:]}")
print(f"NDCG@10s (entrenamiento): {evals_result['validation_0']['ndcg@10'][-5:]}")
print(f"RMSEs (entrenamiento): {evals_result['validation_0']['rmse'][-5:]}")
print(f"AUCs (entrenamiento): {evals_result['validation_0']['auc'][-5:]}")
print()
print(f"MAPs (validación): {evals_result['validation_1']['map'][-5:]}")
print(f"NDCGs (validación): {evals_result['validation_1']['ndcg'][-5:]}")
print(f"NDCG@5s (validación): {evals_result['validation_1']['ndcg@5'][-5:]}")
print(f"NDCG@10s (validación): {evals_result['validation_1']['ndcg@10'][-5:]}")
print(f"RMSEs (validación): {evals_result['validation_1']['rmse'][-5:]}")
print(f"AUCs (validación): {evals_result['validation_1']['auc'][-5:]}")

#-- reporting-- #
