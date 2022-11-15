# -*- coding: utf-8 -*-
"""
"""
from settings import *
from text_utils import *

import importData as importData
import preprocessing as preprocessing
import exploratoryData as exploratoryData
import dataModeling as dataModeling
#from trainModel import *
#from reporting import *

datos = importData.read_data(settings.ruta_feedback)

#-- preprocessing --#
datos = preprocessing.reordering_data(datos_a_corregir= datos)

datos = preprocessing.vectorizing_data(datos_a_procesar = datos,
                                       model_w2v = model_w2v,
                                       pdt = ProcesadorDeTexto()).reset_index()

#-- exploratoryData --#
exploratoryData.exploratoryDataframe(datos) 

#-- dataModeling --#
x_entrna, y_entrna, x_valida, y_valida, x_prueba, y_prueba = dataModeling.split_data(datos_a_dividir = datos, 
                                                                                     p_explr_prueba = .7,
                                                                                     p_entrn_valida = .7,
                                                                                     )

noms_cols_caracts = ['TEXTO_COMPARACION_VECT',
                     'D_EVENTO_VECT',
                     'DIFF_TEXTO_COMPARACION_VECT_&_D_EVENTO_VECT']

feats_entrna, labels_entrna, qids_entrna = dataModeling.obtener_CEQs(X = x_entrna, # Listas con las características, etiquetas y grupos utilizadas en el entrenamiento del modelo
                                                                     y = y_entrna,
                                                                     noms_cols_caracts = noms_cols_caracts)

feats_valida, labels_valida, qids_valida = dataModeling.obtener_CEQs(X =x_valida,
                                                                     y = y_valida,
                                                                     noms_cols_caracts = noms_cols_caracts)

feats_prueba, labels_prueba, qids_prueba = dataModeling.obtener_CEQs(X = x_prueba,
                                                                     y = y_prueba,
                                                                     noms_cols_caracts = noms_cols_caracts)

#-- ModeloXGbosstRanker --#
# -- Hypertuning -- #
from sklearn.model_selection import cross_val_score, KFold
from sklearn.model_selection import GridSearchCV

kfold = KFold(n_splits=5, shuffle=True, random_state=2)

def grid_search(params, xgboost = xgboost.XGBRanker()):

    grid_model = GridSearchCV(xgboost,
                              params,
                              scoring = 'roc_auc',
                              cv = kfold)
    
    grid_model.fit(X = feats_entrna,
                   y = labels_entrna,
                   qid = qids_entrna,
                   eval_set = [(feats_entrna, labels_entrna), 
                               (feats_valida, labels_valida)],
                   eval_qid = [qids_entrna,
                               qids_valida],
                   verbose = False)

    best_params = grid_model.best_params_
    print("Best params:", best_params)

grid_search(params = {'objective': ['rank:ndcg'],
                      'reg_lambda' : [.10, .15, .21, .25, 30],
                      'subsample':[0.3, 0.4, 0.5, 0.6, 0.7]})

###########################
# -- BestModel metrics -- #
###########################
params = {'objective': 'rank:ndcg',
          'reg_lambda' : .1,
          'subsample': 0.3,
          'gamma': .001,
          'missing': -99,
          'eval_metric': ['map','ndcg','ndcg@5','ndcg@10','rmse','auc']}

model_l2r = xgboost.XGBRanker(**params)

model_l2r.fit(X = feats_entrna,
              y = labels_entrna,
              qid = qids_entrna,
              eval_set = [(feats_entrna, labels_entrna), 
                          (feats_valida, labels_valida)],
              eval_qid = [qids_entrna,
                          qids_valida],
              verbose = False)

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

###############
#-- Reporte --#
###############
x_entrna["RANK"] = labels_entrna
x_entrna["y_pred"] = model_l2r.predict(feats_entrna)
x_entrna["rank_l2r"] = (x_entrna.groupby('QID')['y_pred']
                                .rank(method='dense', ascending = True)
                                .astype(int))
x_entrna["datos"] = 'entrenamiento'

#Valida
x_valida["RANK"] = labels_valida
x_valida["y_pred"] = model_l2r.predict(feats_valida)
x_valida["rank_l2r"] = (x_valida.groupby('QID')['y_pred']
                                .rank(method='dense', ascending = True)
                                .astype(int))
x_valida["datos"] = 'valida'

#Prueba
x_prueba["RANK"] = labels_prueba
x_prueba["y_pred"] = model_l2r.predict(feats_prueba)
x_prueba["rank_l2r"] = (x_prueba.groupby('QID')['y_pred']
                                .rank(method='dense', ascending = True)
                                .astype(int))
x_prueba["datos"] = 'prueba'

#Union
datos_l2r = pd.concat([x_entrna, x_valida, x_prueba])

ejemplo_l2r = datos_l2r[(datos_l2r["QID"] == 140) | (datos_l2r["QID"] == 49) | (datos_l2r["QID"] == 39) | (datos_l2r["QID"] == 101)].loc[:,['AM', 'TEXTO_COMPARACION', 'D_EVENTO',
                                                                                                                                             'SIMILITUD', 'EVALUACION', 'QID', 'RANK', 'rank_l2r','datos']]


ejemplo_l2r.columns = ['AM', 'TEXTO_COMPARACION', 'D_EVENTO', 'SIMILITUD', 'EVALUACION', 'QID',
                       'rank_original', 'rank_l2r', 'datos']

entrenamiento_ejemplo = ejemplo_l2r[ejemplo_l2r["datos"] == 'entrenamiento']
valida_ejemplo = ejemplo_l2r[ejemplo_l2r["datos"] == 'valida']
prueba_ejemplo = ejemplo_l2r[ejemplo_l2r["datos"] == 'prueba']

