# -*- coding: utf-8 -*-
"""
"""

import os
os.chdir(r"Code\DataPrep\utils")
from settings import *

os.chdir(r"C:\Users\cflorelu\Documents\1_Ternium\Resumenes-Python\04_Machine Learning Scientist\12_Natural_Lenguague\Model\Code\DataPrep")
import importData as importData
import preprocessing as preprocessing
import exploratoryData as exploratoryData
import dataModeling as dataModeling
from trainModel import *
from reporting import *

os.chdir(r"C:\Users\cflorelu\Documents\1_Ternium\Resumenes-Python\04_Machine Learning Scientist\12_Natural_Lenguague\Model")

datos = importData.read_data(ruta_feedback)

#-- preprocessing --#
experimento = 'Eventos con evaluación == 0'

datos = preprocessing.reordering_data(datos_a_corregir= datos,
                                      evaluaciones_sin_ceros = False) #Si es True (descarta los ceros)

datos = preprocessing.vectorizing_data(datos_a_procesar = datos,
                                       model_w2v = model_w2v,
                                       pdt = ProcesadorDeTexto()).reset_index()

#-- exploratoryData --#
#exploratoryData.exploratoryDataframe(datos) 

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

feats_valida, labels_valida, qids_valida = dataModeling.obtener_CEQs(X = x_valida,
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
                              scoring = 'top_k_accuracy',
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

tmp = datos_l2r[datos_l2r["QID"] == 1].loc[:,["D_EVENTO", "rank_l2r"]]

#Rank similitud
import numpy as np
from sklearn.metrics import ndcg_score

datos_l2r['rank_w2v'] = datos_l2r.groupby("QID")["SIMILITUD"].rank('first', ascending =  False)
datos_l2r['rank_w2v'] = datos_l2r['rank_w2v'].astype(int)
datos_l2r['RANK'] = datos_l2r['RANK'].astype(int)

#ndcg por grupo QID
qid = list(set(datos_l2r["QID"]))

ndcg_l2r = []
ndcg_w2v = []

qids = []
dato = []

for i in range(len(qid)):
    
    dat = datos_l2r[datos_l2r["QID"] == qid[i]]['datos'].unique()[0]
    rank_origin = np.asarray([list(datos_l2r[datos_l2r["QID"] == qid[i]].loc[:,['RANK']]['RANK'])])
    rank_l2r = np.asarray([list(datos_l2r[datos_l2r["QID"] == qid[i]].loc[:,['rank_l2r']]['rank_l2r'])])
    rank_w2v = np.asarray([list(datos_l2r[datos_l2r["QID"] == qid[i]].loc[:,['rank_w2v']]['rank_w2v'])])
    
    dato.append(dat)
    qids.append(qid[i])
    
    if rank_origin.shape[1] == 1:
        
        ndcg_l2r.append(1)
        ndcg_w2v.append(1)

    else:
        
        ndcg_l2r.append(ndcg_score(rank_l2r, rank_origin))
        ndcg_w2v.append(ndcg_score(rank_w2v, rank_origin))

df_ndcg = pd.DataFrame(zip(qids, ndcg_l2r, ndcg_w2v, dato),
                       columns = ['qids','ndcg_l2r', 'ndcg_w2v','dato'])

df_ndcg['dif_ndcg'] = df_ndcg['ndcg_l2r'] - df_ndcg['ndcg_w2v']

df_ndcg.groupby(["dato"]).agg({'ndcg_l2r':'mean'})
df_ndcg.groupby(["dato"]).agg({'ndcg_w2v':'mean'})

#Histograma
df = df_ndcg.loc[:,["dato","ndcg_l2r", "ndcg_w2v"]]

df = df.melt(id_vars=['dato'], 
             value_vars=["ndcg_l2r", "ndcg_w2v"])

import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="darkgrid", palette=None)

sns.displot(
    df,
    x = "value",
    col="dato",
    row="variable",
    facet_kws=dict(margin_titles=True),
    height=3,
    aspect=.7
)
plt.show()

#Diferencia
import plotly.express as px

fig = px.bar(df_ndcg,
             x = "qids",
             y = "dif_ndcg",
             color = 'dato',
             title = "{}, diferencia NDCG entre L2R y W2V. <br><sup> L2R mejor en {}, W2V mejor en {}, iguales en {} </sup>".format(experimento,
                                                                                                                                    sum(df_ndcg['dif_ndcg'] > 0),
                                                                                                                                    sum(df_ndcg['dif_ndcg'] < 0),
                                                                                                                                    sum(df_ndcg['dif_ndcg'] == 0)),
             height=300)

fig.show()

#Ejemplos
