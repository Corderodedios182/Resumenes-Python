# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 12:39:02 2022

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

#-- exploratoryData --#
exploratoryDataframe(datos)

#-- dataModeling --#
x_entrna, y_entrna, x_valida, y_valida, x_prueba, y_prueba = split_data(datos_a_dividir = datos,
                                                                        p_explr_prueba = .8,
                                                                        p_entrn_valida = .8,
                                                                        )

noms_cols_caracts = ['TEXTO_COMPARACION_VECT',
                     'D_EVENTO_VECT',
                     'DIFF_TEXTO_COMPARACION_VECT_&_D_EVENTO_VECT']

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

# -- BestModel metrics -- #

params = {'objective': 'rank:ndcg',
          'reg_lambda' : .21,
          'subsample': 0.4,
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

# -- Reportes -- #

#Entrenamiento

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

#Safety Analytics : Función def output_predict(data_input):
    
#    return lista_ordenada_consulta

#TextUpdater : Nuevo entrenamiento
    
#Porcentaje de datos representativos
#    
    
    
    
    
    
    
    
    
    
    
    
    
