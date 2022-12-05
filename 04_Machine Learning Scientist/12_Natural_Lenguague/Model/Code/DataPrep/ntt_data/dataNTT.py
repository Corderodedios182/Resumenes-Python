# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 09:51:13 2022

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

#--Data original --#
df_origin = importData.read_data(ruta_feedback)
df_origin["C_EVENTO_UNIQUE"] = df_origin["TEXTO_COMPARACION"] + " - " + df_origin["D_EVENTO"]

tmp = df_origin["TEXTO_COMPARACION"] + " - " + df_origin["D_EVENTO"]
tmp = pd.DataFrame(tmp.drop_duplicates())
tmp["C_EVENTO_NEW"] = list(range(tmp.shape[0]))
tmp.columns = ["C_EVENTO_UNIQUE","C_EVENTO_NEW"]

df_origin = df_origin.merge(tmp,
                            on = 'C_EVENTO_UNIQUE')

df_origin

#df_origin["AM-C_EVENTO_UNIQUE"] = df_origin["AM"].astype(str) + "-" + df_origin["C_EVENTO_UNIQUE"].astype(str)

#--Data vectorizada --#
df_vect = importData.read_data(ruta_feedback)

df_vect = preprocessing.reordering_data(datos_a_corregir = df_vect,
                                        evaluaciones_sin_ceros = False)

df_vect = preprocessing.vectorizing_data(datos_a_procesar = df_vect,
                                         model_w2v = model_w2v,
                                         pdt = ProcesadorDeTexto())

df_vect = df_vect.loc[:,['C_EVENTO_NEW', 'C_EVENTO_UNIQUE', "TEXTO_COMPARACION_VECT", "D_EVENTO_VECT", "DIFF_TEXTO_COMPARACION_VECT_&_D_EVENTO_VECT"]]

#df_vect.to_csv("datos_vec.csv")
#df_origin.to_csv("df_origin.csv")

#
tmp = df_origin.loc[:,["C_EVENTO","D_EVENTO", "TEXTO_COMPARACION"]].drop_duplicates()
tmp["contador"] = 1
tmp = tmp.groupby(["C_EVENTO","D_EVENTO", "TEXTO_COMPARACION"]).count()

df_ntt = df_origin.merge(df_vect,
                         left_on = 'C_EVENTO_NEW',
                         right_on = 'C_EVENTO_NEW',
                         how = 'left')

tmp = df_origin.loc[:,["AM", "C_EVENTO", "C_EVENTO_NEW", "D_EVENTO", "TEXTO_COMPARACION"]].drop_duplicates()
tmp["contador"] = 1
tmp = tmp.groupby(["AM", "C_EVENTO"]).count()


