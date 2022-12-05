# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 13:31:06 2022

Solo se tomaron eventos con evaluaciones !=0 

@author: cflorelu
"""
from settings import *
from text_utils import *

import importData as importData
import preprocessing as preprocessing
import exploratoryData as exploratoryData
import dataModeling as dataModeling
#from trainModel import *
#from reporting import *

datos = importData.read_data(ruta_feedback)

#-- preprocessing --#
experimento = 'Eventos con evaluación == 0'

datos = preprocessing.reordering_data(datos_a_corregir= datos,
                                      evaluaciones_sin_ceros = False) #Si es True (descarta los ceros)

datos = preprocessing.vectorizing_data(datos_a_procesar = datos,
                                       model_w2v = model_w2v,
                                       pdt = ProcesadorDeTexto()).reset_index()

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

###############
#-- Reporte --#
###############
x_entrna["RANK"] = labels_entrna
x_entrna["y_pred"] = model_l2r.predict(feats_entrna)
x_entrna["rank_l2r"] = (x_entrna.groupby('QID')['y_pred']
                                .rank(method='dense', ascending = False)
                                .astype(int))
x_entrna["datos"] = 'entrenamiento'

#Valida
x_valida["RANK"] = labels_valida
x_valida["y_pred"] = model_l2r.predict(feats_valida)
x_valida["rank_l2r"] = (x_valida.groupby('QID')['y_pred']
                                .rank(method='dense', ascending = False)
                                .astype(int))
x_valida["datos"] = 'valida'

#Prueba
x_prueba["RANK"] = labels_prueba
x_prueba["y_pred"] = model_l2r.predict(feats_prueba)
x_prueba["rank_l2r"] = (x_prueba.groupby('QID')['y_pred']
                                .rank(method='dense', ascending = False)
                                .astype(int))
x_prueba["datos"] = 'prueba'

#Union
datos_l2r = pd.concat([x_entrna, x_valida, x_prueba])

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

rel = sns.displot(df,
                  x = "value",
                  col="dato",
                  row="variable",
                  facet_kws=dict(margin_titles=True),
                  height=3,
                  aspect=.7)

rel.fig.subplots_adjust(top = .9)
rel.fig.suptitle('{}'.format(experimento))

#############################################
#¿Como está rankeando los valores + , - y 0?#
#############################################

df_ndcg

round(datos_l2r["EVALUACION_SUM"].value_counts(normalize = True),2)

datos_l2r.columns
datos_l2r = datos_l2r.drop(['TEXTO_COMPARACION_VECT', 'D_EVENTO_VECT',
                            'DIFF_TEXTO_COMPARACION_VECT_&_D_EVENTO_VECT'], axis = 1)

datos_l2r.loc[datos_l2r["EVALUACION_SUM"] == 0, 'eventos_sin_feedback'] = 1

datos_l2r["dif_rank_l2r"] = abs(datos_l2r["RANK"] - datos_l2r["rank_l2r"])
datos_l2r["dif_rank_w2v"] = abs(datos_l2r["RANK"] - datos_l2r["rank_w2v"])

datos_l2r["n_eventos"] = 1

tmp = datos_l2r.groupby(["QID","datos"], as_index = False).agg({"dif_rank_l2r":"sum",
                                                                "dif_rank_w2v":"sum",
                                                                "n_eventos":"count",
                                                                "eventos_sin_feedback":"sum"})

tmp["evento_feedback"] = tmp["n_eventos"] - tmp["eventos_sin_feedback"]

tmp = tmp.loc[:,["QID", "eventos_sin_feedback","evento_feedback"]]

tmp = pd.concat([df_ndcg, tmp], axis = 1).loc[:,["QID","ndcg_l2r","ndcg_w2v","eventos_sin_feedback","evento_feedback"]]

tmp = tmp.melt(value_vars = ["eventos_sin_feedback","evento_feedback", "ndcg_l2r",  "ndcg_w2v"], id_vars = "QID")

#Gráfica

ndcg = tmp[tmp["variable"].str.contains('ndcg')]
conteo = tmp[~(tmp["variable"].str.contains('ndcg'))]

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

matplotlib.rc_file_defaults()
ax1 = sns.set_style(style=None, rc=None )

fig, ax1 = plt.subplots(figsize=(20,10))

sns.lineplot(data = ndcg[ndcg["QID"] < 50],
             x = 'QID',
             y = 'value',
             hue = 'variable',
             marker='o',
             sort = False,
             ax = ax1,
             )
ax2 = ax1.twinx()

sns.barplot(data = conteo[conteo["QID"] < 50],
            x = 'QID',
            y = 'value',
            hue = 'variable',
            alpha = 0.5,
            ax = ax2)
plt.show()

ejemplo = datos_l2r[datos_l2r["QID"] == 75].drop(["y_pred","datos","valor_ceros","n_eventos","rank_w2v","dif_rank_w2v","SIMILITUD"], axis = 1)
ejemplo = datos_l2r[datos_l2r["QID"] == 75].drop(["y_pred","datos","valor_ceros","n_eventos","rank_l2r","dif_rank_l2r","SIMILITUD"], axis = 1)

#Ejemplos
#datos_l2r_con_ceros = datos_l2r
#datos_l2r_sin_ceros = datos_l2r

#ejemplo_l2r = datos_l2r[(datos_l2r["QID"] == 6) | (datos_l2r["QID"] == 49) | (datos_l2r["QID"] == 39) | (datos_l2r["QID"] == 101)].loc[:,['AM', 'TEXTO_COMPARACION', 'D_EVENTO',
#                                                                                                                                          'SIMILITUD', 'EVALUACION_SUM', 'QID',
#                                                                                                                                          'RANK', 'rank_l2r','datos']]
#ejemplo_l2r.columns = ['AM', 'TEXTO_COMPARACION', 'D_EVENTO', 'SIMILITUD', 'EVALUACION', 'QID',
#                       'rank_original', 'rank_l2r', 'datos']

#entrenamiento_ejemplo = ejemplo_l2r[ejemplo_l2r["datos"] == 'entrenamiento']
#valida_ejemplo = ejemplo_l2r[ejemplo_l2r["datos"] == 'valida']
#prueba_ejemplo = ejemplo_l2r[ejemplo_l2r["datos"] == 'prueba']


















