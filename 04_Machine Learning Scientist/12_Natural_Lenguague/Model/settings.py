# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 12:20:51 2022

@author: cflorelu
"""

## • Módulos a Importar ########################################################
################################################################################
# region


### Estándar
####  - configparser: Módulo usado para acceder a las configuraciones globales 
####                   del proyecto
####  - IPython.display: _descripción_
####  - math: Se utiliza para invocar función sqrt
####  - logging: Se utiliza para ejecutar la bitácora
####  - pprint: Provides a capability to “pretty-print” arbitrary Python data 
####             structures in a form which can be used as input to the
####             interpreter
####  - statistics: Se utiliza para importar funciones promedio y desviación 
####                  estándar
####  - typing: módulo usado para proveer indicios de tipificación de variables
####  - warnings: módulo usado para ignorar avisos de advertencia
import configparser
from IPython.display import display
from math import sqrt
import logging
import pprint
from statistics import mean, stdev
from typing import Dict, List, Tuple, Union
import warnings
warnings.filterwarnings("ignore")


### De terceros
####  - gensim: Módulo para procesar texto, similitudes, vectorizar
####  - numpy: Con este módulo se manejan arreglos de numpy y métodos de 
####            promediado y suma de vectores p/elemento
####  - pandas: _descripción_
####  - sklearn.metrics: _descripción_
####  - sklearn.model_selection: _descripción_
####  - xgboost: Módulo con modelos de datos entrenados por medio de boosting
import gensim
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, ndcg_score
from sklearn.model_selection import GroupShuffleSplit
import xgboost


### Local
####  - utils.broker: Módulo usado para acceder a archivos en MS Azure Storage
####  - utils.settings: Módulo usado para invocar datos generales del proyecto
####  - utils.text_utils: Módulo usado para hacer procesamiento de texto
#import utils.broker as bk
#import utils.settings as s
from text_utils import *

config = configparser.ConfigParser()
config.read('sistema.config', encoding='utf-8')

ruta_feedback = config['PATHS']['feedback']

url = config['BLOB_STORAGE_FEEDBACK']['url']
container = config['BLOB_STORAGE_FEEDBACK']['container']
shared_access_key = config['BLOB_STORAGE_FEEDBACK']['shared_access_key']

model_w2v = gensim.models.word2vec.Word2Vec.load(fname='models/w2v/model_w2v.model')
