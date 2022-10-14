# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 13:42:54 2022

@author: cflorelu
"""
from IPython.display import display
from typing import Dict, List, Tuple, Union
import warnings
warnings.filterwarnings("ignore")

import gensim
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, ndcg_score
from sklearn.model_selection import GroupShuffleSplit
import xgboost

import utils.text_utils as text_utils

# Métodos Auxiliares #
######################

def _map_score(
    y_prueba: List,
) -> float:
    """Función que entrega la puntuación MAP (Mean Average Precision)

    Parameters
    ----------
    y_prueba : _type_
        _description_
            
    Returns
    -------
    float
        _description_
    """

    # Transformación de valores flotantes a valores enteros ordinarios
    y_perfecto = sorted(y_prueba.copy())
    y_perfecto = [ 1 if value>=0.5 else 0 for value in y_perfecto ]

    y_perfecto = np.array(y_perfecto)
    y_prueba = np.array(y_prueba)
    
    
    map_ = \
        average_precision_score(
            y_true=y_perfecto,
            y_score=y_prueba,
        )
    
    return map_


def _ndcg_score(
    y_verdadero: List,
    y_puntuación: List,
) -> float:

    # Transformación de valores flotantes a valores enteros ordinarios
    values = set(y_verdadero)
    values = list(values)
    values.sort()
    traductor = { value: key for key, value in enumerate(values) }
    n_y_verdadero = [ traductor[old_value] for old_value in y_verdadero ]

    n_y_verdadero = np.array([n_y_verdadero])
    y_puntuación = np.array([y_puntuación])
    
    
    ndcg_ = \
        ndcg_score(
            y_true=n_y_verdadero,
            y_score=y_puntuación,
            #k=10,
        )
    
    return ndcg_


def importar_datos(
    ruta_al_archivo: str,
) -> pd.DataFrame:
    """Importa los datos de archivo local.
    Procesa los datos y los entrega en forma de DataFrame.
    Formato de datos: 
        https://xgboost.readthedocs.io/en/stable/tutorials/input_format.html

    Parameters
    ----------
    ruta_al_archivo : str
        Ruta al archivo.

    Returns
    -------
    pd.DataFrame
        _description_
    """
    
    datos = \
        pd.read_parquet(
            path=ruta_al_archivo,
        )
    
    return datos


def corregir_datos(
    datos_a_corregir: pd.DataFrame,
) -> pd.DataFrame:
    """Aquí se quitan las filas duplicadas que no recibieron retroalimentación,
    a excepción de la primera que no recibió retroalimentación.

    Parameters
    ----------
    datos_a_corregir: pd.DataFrame
        _description_
    
    Returns
    -------
    pd.DataFrame
        _description_
    """
    
    datos_a_corregir.reset_index(
        inplace=True,
    )
    
    datos_a_corregir.drop(
        columns=['index', 'ID_EVALUACION'],
        inplace=True,
    )

    # Ordenamiento de datos para facilitar el uso de métodos con grupos
    datos_a_corregir.sort_values(
        by=['TEXTO_COMPARACION', 'F_CREATE', 'INDICE'],
        inplace=True,
    )
    
    # Diccionarios utilitarios, ayudarán más adelante a dar formato a ciertos datos
    textos_comparacion_únicos = \
        datos_a_corregir['TEXTO_COMPARACION'].unique()
        
    textos_comparacion_únicos = \
        textos_comparacion_únicos.tolist()
        
    textos_comparacion_idx_dicc = \
        {
            elem: idx
            for (idx, elem)
            in enumerate(
                iterable=textos_comparacion_únicos,
                start=1,
            )
        }

    # Creación de la columna QID (de identificación), utiliza valores de la columna
    # TEXTO_COMPARACION reemplazando el texto de consulta por un número
    datos_a_corregir['QID'] = \
        datos_a_corregir[['TEXTO_COMPARACION']].replace(
            to_replace=textos_comparacion_idx_dicc,
        )

    # Reordenamiento de columnas
    datos_a_corregir = \
        datos_a_corregir[
            [
                'AM',
                'USR_EVALUACION',
                'PROCESADO',
                'F_CREATE',
                'TEXTO_COMPARACION',
                'SIMILITUD',
                'INDICE',
                'C_EVENTO', 
                'D_EVENTO',
                'EVALUACION',
                'QID',
            ]
        ]

    
    # Aquí se suman todos los C_EVENTO correspondiente a su grupo QID
    datos_a_corregir['EVALUACION'] = \
        datos_a_corregir.groupby(
            by=['C_EVENTO', 'QID', ]
        )['EVALUACION'].transform('sum')

    # Se borran los que están duplicados, dado que ya se sumaron todas las 
    #  instancias
    datos_a_corregir = \
        datos_a_corregir.drop_duplicates(
            subset = \
                [
                    'D_EVENTO',
                    'TEXTO_COMPARACION',
                    'EVALUACION',
                    'USR_EVALUACION',
                    'PROCESADO',
                    'QID',
                ],
            keep='first',
        )
    
    #-REFACTOR: QUITAR ESTE PEDAZO
    # Normalización: 
    #   Se agrega la mínima evaluación, y se divide entre la mayor cantidad de 
    #    evaluaciones sumadas, así quedan los valores en el rango [0, 1]
    datos_a_corregir['EVALUACION'] = \
        datos_a_corregir['EVALUACION'] \
        + abs(datos_a_corregir['EVALUACION'].min())
    
    datos_a_corregir['EVALUACION'] = \
        datos_a_corregir['EVALUACION'] \
        / datos_a_corregir['EVALUACION'].max()
    
    return datos_a_corregir


## -Preprocesamiento de datos adhoc al modelo
def preprocesar_datos(
    datos_a_procesar: pd.DataFrame,
    model_w2v: gensim.models.word2vec.Word2Vec,
    pdt: text_utils.ProcesadorDeTexto,
) -> pd.DataFrame:
    """Vectorización de documentos, consultas y operaciones de extracción de 
     características.

    Parameters
    ----------
    datos_a_procesar: pd.DataFrame
        _description_
    pdt: new_text_utils.ProcesadorDeTexto
        _description_
    model_w2v: gensim.models.word2vec.Word2Vec
        _description_

    Returns
    -------
    pd.DataFrame
        _description_
    """
    
    datos_a_procesar.drop(
        columns = \
            [
                'AM',
                'F_CREATE',
                'PROCESADO',
                'USR_EVALUACION',
            ],
            inplace=True,
        )
        
    datos_a_procesar['TEXTO_COMPARACION_VECT'] = \
        datos_a_procesar['TEXTO_COMPARACION'].apply(
            func=pdt.vectorize,
            model_w2v=model_w2v,
        )
        
    datos_a_procesar['D_EVENTO_VECT'] = \
        datos_a_procesar['D_EVENTO'].apply(
            func=pdt.vectorize,
            model_w2v=model_w2v,
        )
        
    datos_a_procesar['DIFF_TEXTO_COMPARACION_VECT_&_D_EVENTO_VECT'] = \
        datos_a_procesar['TEXTO_COMPARACION_VECT'].apply(np.array) \
        - datos_a_procesar['D_EVENTO_VECT'].apply(np.array)

    # datos_a_procesar['BM25'] = \
    #     datos_a_procesar['TEXTO_COMPARACION'].apply(
    #         func=pdt.vectorize,
    #         model_w2v=model_w2v,
    #     )
        
    return datos_a_procesar


## -División de datos - Exploración y Prueba
def dividir_conj_datos(
    datos_a_dividir: pd.DataFrame,
    p_explr_prueba: float,
    p_entrn_valida: float,
) -> \
    Tuple[
        pd.DataFrame,
        pd.DataFrame,
        pd.DataFrame,
        pd.DataFrame,
        pd.DataFrame,
        pd.DataFrame,
    ]:
    """Dividir conjunto de datos en Exploración (Entrenamiento, Validación) y 
     Prueba.

    █ Conjunto de Datos ████████████████████████████████\n
    █ Datos Exploración ██████████████████│█ D. Prueba █\n
    █ D. Entrenamiento ██████│█ D. Valid █│█ D. Prueba █\n

    Parameters
    ----------
    datos_a_dividir : pd.DataFrame
        Conjuntos de datos
    p_explr_prueba: float
        Proporción de datos que pertenecerán a exploración y a prueba [0, 1]
    p_entrn_valida: float
        Proporción de datos que pertenecerán a entrenamiento y validación [0, 1]

    Returns
    -------
    Tuple[
        pd.DataFrame, pd.DataFrame,
        pd.DataFrame, pd.DataFrame,
        pd.DataFrame, pd.DataFrame,
    ]
        x_entrna, y_entrna, x_valida, y_valida, x_prueba, y_prueba
    """

    # División en Datos de Exploración y Datos de Prueba
    gss_explra_prueba = \
        GroupShuffleSplit(
            train_size=p_explr_prueba,
            n_splits=1,
        ).split(
            datos_a_dividir,
            groups=datos_a_dividir['QID'],
        )

    inds_X_explra, inds_X_prueba = \
        next(gss_explra_prueba)

    datos_explra = \
        datos_a_dividir.iloc[inds_X_explra]
    datos_prueba = \
        datos_a_dividir.iloc[inds_X_prueba]

    # División en Datos de Entrenamiento y Datos de Validación
    gss_entrn_valida = \
        GroupShuffleSplit(
            train_size=p_entrn_valida,
            n_splits=1,
        ).split(
            datos_explra,
            groups=datos_explra['QID'],
        )

    inds_X_entrna, inds_X_valida = \
        next(gss_entrn_valida)

    datos_entrna = \
        datos_explra.iloc[inds_X_entrna]
    datos_valida = \
        datos_explra.iloc[inds_X_valida]
    
    x_entrna = \
        datos_entrna.loc[:, ~datos_entrna.columns.isin(['EVALUACION'])]
    y_entrna = \
        datos_entrna.loc[:,  datos_entrna.columns.isin(['EVALUACION'])]
    x_valida = \
        datos_valida.loc[:, ~datos_valida.columns.isin(['EVALUACION'])]
    y_valida = \
        datos_valida.loc[:,  datos_valida.columns.isin(['EVALUACION'])]
    x_prueba = \
        datos_prueba.loc[:, ~datos_prueba.columns.isin(['EVALUACION'])]
    y_prueba = \
        datos_prueba.loc[:,  datos_prueba.columns.isin(['EVALUACION'])]
    
    return x_entrna, y_entrna, x_valida, y_valida, x_prueba, y_prueba


## -División de datos - Características, Etiquetas, QIDs
def obtener_CEQs(
    X: pd.DataFrame,
    y: pd.DataFrame,
    noms_cols_caracts: List[str],
) -> \
Tuple[
    np.ndarray,
    pd.Series,
    pd.Series,
]:
    """División de los dataframe en columnas específicas.
    Esto para que el modelo pueda aceptar los datos.

    Parameters
    ----------
    X : pd.DataFrame
        _description_
    y : pd.DataFrame
        _description_
    noms_cols_caracts : List[str]
        _description_

    Returns
    -------
    Tuple[np.ndarray, pd.Series, pd.Series]
        _description_
    """
    
    # Características del conjunto de datos
    caracts = \
        [
            np.vstack(X[nom_columna])
            for nom_columna
            in noms_cols_caracts
        ]
    
    caracts= np.hstack(caracts)
    
    etiquetas = y['EVALUACION']
    qids = X['QID']
    
    return caracts, etiquetas, qids


##  -Experimentación con modelo
def entrenamiento(
    noms_cols_caracts: List[str],
    params: Dict[str, Union[str, int, float]],
    feats_entrena: np.ndarray,
    feats_valida: np.ndarray,
    labels_entrena: pd.Series,
    labels_valida: pd.Series,
    qids_entrena: pd.Series,
    qids_valida: pd.Series,
) -> xgboost.XGBRanker:
    """Aquí se ejecuta un experimento con parámetros modificables del modelo 
     xgboost.XGBRanker.

    Parameters
    ----------
    noms_cols_caracts : _type_
        _description_
    params : Dict[str, Union[str, int, float]]
        _description_
    feats_entrena : np.ndarray
        _description_
    feats_prueba : np.ndarray
        _description_
    labels_entrena : pd.Series
        _description_
    labels_prueba : pd.Series
        _description_
    qids_entrena : pd.Series
        _description_
    qids_prueba : pd.Series
        _description_
    """

    ##  • Inicialización y entrenamiento de modelo L2R
    print(f'noms_columnas_características: {noms_cols_caracts}\n')
    
    model_l2r = \
        xgboost.XGBRanker(
            **params
        )

    model_l2r.fit(
        X = feats_entrena,
        y = labels_entrena,
        qid = qids_entrena,
        eval_set = \
            [
                (feats_entrena, labels_entrena), 
                (feats_valida, labels_valida)
            ],
        eval_qid = \
            [
                qids_entrena,
                qids_valida,
            ],
        verbose = False,
    )

    evals_result = \
        model_l2r.evals_result()

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

    return model_l2r


##  -Funciones para visualizar resultados
def estilizador_color_max_min(
    df: pd.DataFrame,
    slice: List[str]
):
    def highlight_max(
        s,
        props=''
    ):
        return np.where(s==np.nanmax(s.values), props, '')

    def highlight_min(
        s,
        props=''
    ):
        return np.where(s==np.nanmin(s.values), props, '')

    styler = \
        df.style \
        .apply(
            func=highlight_max, 
            props='background-color:lightblue;',
            axis=0,
            subset=slice
        ).apply(
            func=highlight_min,
            props='background-color:pink;',
            axis=0,
            subset=slice
        )
            
    return styler


def plot_resultados(
    x: pd.DataFrame,
    y: pd.DataFrame,
    feats: np.ndarray,
    l2r_actual: xgboost.XGBRanker,
    noms_cols_caracts: List[str],
    consulta: str='',
    ordenar_con_l2r: bool=True,
) -> pd.DataFrame:
    """Graficar resultados del modelo l2r.

    Parameters
    ----------
    x : pd.DataFrame
        _description_
    y : pd.DataFrame
        _description_
    feats : np.ndarray
        _description_
    l2r_actual : xgboost.XGBRanker
        _description_
    noms_cols_caracts : List[str]
        _description_
    consulta : str = None
        _description_
    ordenar_con_l2r : bool
        _description_
    Returns
    -------
    pd.DataFrame,
    """

    # Si no se proveyó consulta, entonces se elige una al azar
    if consulta == '':
        # Se elige una cadena de caracteres aleatoria a partir de los textos en
        #  x
        consulta = \
            np.random.choice(
                a=x['TEXTO_COMPARACION'].unique()
            )
    # Se imprime en consola
    print(f"Consulta: '\033[38;2;0;100;255m{consulta}\033[38;2;255;255;255m\033\
[0m'")

    # Se piden predicciones al modelo con las características de cada texto
    # (feats) y se crea un nuevo DataFrame
    preds = \
        l2r_actual.predict(
            X=feats
        )
        
    preds_df = \
        pd.DataFrame(
            data=preds,
            columns=['ORDEN_L2R'],
            index=x.index,
        )

    # Se crea un DataFrame a partir del conjunto x, las etiquetas y las 
    #  predicciones de puntuación preds
    results_consulta = \
        pd.concat(
            objs=[x, y, preds_df],
            axis=1,
        )
    
    # Si se tiene ordenar_con_l2r como verdadero, se ordena usando el modelo l2r
    if ordenar_con_l2r:
        # y se ordenan a partir de la columna 0 que es la columna que almacena 
        #  las puntuaciones dadas por el modelo a cada renglón de 
        #  características
        lista_de_orden = ['ORDEN_L2R', 'EVALUACION']
    # En caso contrario, se ordena con la similitud coseno
    else:
        lista_de_orden = ['SIMILITUD']
        
    results_consulta = \
        results_consulta[results_consulta['TEXTO_COMPARACION']==consulta] \
            .sort_values(
                by=lista_de_orden,
                ascending=False
            )

    # Se imprime la cantidad de documentos relacionados a la consulta elegida
    #  anteriormente
    print(f"Cantidad de documentos: '\033[38;2;0;200;0m\
{results_consulta.shape[0]}\033[38;2;255;255;255m\033[0m'")

    # Con la lista de columnas se quitan columnas que podrían causar ruido, se
    #  eliminan esas columnas y se invoca una función para darle formato al 
    #  DataFrame
    results_consulta.drop(
        columns=noms_cols_caracts,
        inplace=True
    )
    
    results_consulta_estilizado = \
        estilizador_color_max_min(
            df=results_consulta,
            slice=['EVALUACION']
        )

    # Se muestra el dataframe estilizado con los documentos relacionados a la
    #  consulta
    display(results_consulta_estilizado)
    
    return results_consulta


# Experimento i - <Conjunto J>; <Consulta K>;
def plot_resultados_completos(
    i_experimento: int,
    x: pd.DataFrame,
    y: pd.DataFrame,
    feats: np.ndarray,
    l2r_actual: xgboost.XGBRanker,
    noms_cols_caracts: List[str],
    consulta: str='',
) -> \
    Tuple[
        pd.DataFrame,
        pd.DataFrame,
        float,
        float
    ]:

    ## Si la consulta sigue como valor por defecto: ''
    ## Se elige el i_experimento-ésimo valor del conjunto de datos x
    if consulta=='':
        lista_de_consultas = x['TEXTO_COMPARACION'].value_counts()
        consulta = lista_de_consultas.index[i_experimento]

    resultados_simcos = \
        plot_resultados(
            x=x, 
            y=y, 
            feats=feats,
            l2r_actual=l2r_actual,
            noms_cols_caracts=noms_cols_caracts,
            consulta=consulta,
            ordenar_con_l2r=False,
        )

    resultados_l2r = \
        plot_resultados(
            x=x, 
            y=y, 
            feats=feats,
            l2r_actual=l2r_actual,
            noms_cols_caracts=noms_cols_caracts,
            consulta=consulta,
            ordenar_con_l2r=True,
        )


    # Se calcula la métrica de ordenamiento tanto de similtud cos, como de l2r
    evaluaciones_simcos = resultados_simcos['EVALUACION'].to_list()
    ord_simcos = resultados_simcos['SIMILITUD'].to_list()
    metrc_simcos = \
        _ndcg_score(
            y_verdadero=evaluaciones_simcos,
            y_puntuación=ord_simcos
        )

    evaluaciones_l2r = resultados_l2r['EVALUACION'].to_list()
    ord_l2r = resultados_l2r['ORDEN_L2R'].to_list()
    metrc_l2r = \
        _ndcg_score(
            y_verdadero=evaluaciones_l2r,
            y_puntuación=ord_l2r
        )

    # Se imprimen valores en consola
    print(f'ndcg_simcos = {metrc_simcos}')
    print(f'ndcg_l2r = {metrc_l2r}')


    resultados_simcos.reset_index(inplace=True)
    resultados_l2r.reset_index(inplace=True)

    resultados_simcos.drop(
        columns = \
            [
                'C_EVENTO',
                'INDICE',
                'ORDEN_L2R',
                'QID',
                'TEXTO_COMPARACION',
            ],
        inplace=True,
        )
    resultados_l2r.drop(
        columns = \
            [
                'C_EVENTO',
                'INDICE',
                'QID',
                'SIMILITUD',
                'TEXTO_COMPARACION',
            ],
        inplace=True,
        )

    resultados_juntos = \
        pd.concat(
            objs=[resultados_simcos, resultados_l2r],
            axis=1,
        )

    resultados_juntos.to_csv(f'resultados{i}{i_experimento}.csv')

    r = resultados_juntos.style\
        .set_table_attributes("style='display:inline'")\
        .set_caption(f'Experimento {i_experimento+1} - Conjunto de Entrenamiento; Consulta: {consulta}')

    # Mostrar tabla de resultados simcos y l2r
    display(r)
    
    return resultados_simcos, resultados_l2r, metrc_simcos, metrc_l2r

# endregion
