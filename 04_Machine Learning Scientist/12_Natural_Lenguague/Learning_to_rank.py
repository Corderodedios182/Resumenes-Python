# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 09:59:22 2022

@author: cflorelu
"""

import configparser
from IPython.display import display
from math import sqrt
import logging
import pprint
from statistics import mean, stdev
from typing import Dict, List, Tuple, Union
import warnings
warnings.filterwarnings("ignore")

import gensim
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, ndcg_score
from sklearn.model_selection import GroupShuffleSplit
import xgboost

import utils.broker as bk
import utils.settings as s
import utils.text_utils as text_utils
import utils.function_utils as futils

################
# Configuración#

config = configparser.ConfigParser()
config.read('config/sistema.config', encoding='utf-8')

ruta_feedback = config['PATHS']['feedback']

url = config['BLOB_STORAGE_FEEDBACK']['url']
container = config['BLOB_STORAGE_FEEDBACK']['container']
shared_access_key = config['BLOB_STORAGE_FEEDBACK']['shared_access_key']

logging.basicConfig(
    level = logging.INFO,
    filename = 'xgb.log',
    filemode = 'w',
    format = '%(name)s - %(levelname)s - %(message)s'
)

##############
#Data extract#

feedback = \
    bk.download_from_blob(
        url=url,
        container=container,
        shared_access_key=shared_access_key,
        blob_file_name='búsquedas_con_retro.parquet'
    )
    
feedback.to_parquet(
    path=ruta_feedback,
    engine='auto'
)

##########
# Modelos#

model_w2v = \
    gensim.models.word2vec.Word2Vec

pdt = \
    text_utils.ProcesadorDeTexto()
    
model_l2r = \
    xgboost.XGBRanker()
    
#######
# Main#

datos = futils.importar_datos(ruta_feedback)

datos = futils.corregir_datos(datos_a_corregir=datos)

datos = futils.preprocesar_datos(datos_a_procesar=datos,
                           model_w2v=model_w2v,
                           pdt=pdt)

x_entrna, y_entrna, x_valida, y_valida, x_prueba, y_prueba = futils.dividir_conj_datos(datos_a_dividir=datos,
                                                                                       p_explr_prueba=.90,
                                                                                       p_entrn_valida=.89)

noms_cols_caracts = ['TEXTO_COMPARACION_VECT',                       # Este es el query
                     'D_EVENTO_VECT',                                # Aquí es el vec del documento
                     'DIFF_TEXTO_COMPARACION_VECT_&_D_EVENTO_VECT',  # La diferencia escalar entre vectores
                     #'ELEMS_MÁS_DIFF'
                     #'Zona de evento'
                     #'País'
                     ]
