# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 13:04:30 2022

@author: cflorelu
"""
from settings import *

def reordering_data(
    datos_a_corregir: pd.DataFrame,
    evaluaciones_sin_ceros = True
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
    
    if evaluaciones_sin_ceros == True:
        datos_a_corregir = datos_a_corregir[datos_a_corregir["EVALUACION"] != 0]
        
    datos_a_corregir["AM-C_EVENTO"] = datos_a_corregir["AM"].astype(str) + "-" + datos_a_corregir["C_EVENTO"].astype(str)
    datos_a_corregir["AM-TEXTO_COMPARACION"] = datos_a_corregir["AM"].astype(str) + "-" + datos_a_corregir["TEXTO_COMPARACION"].astype(str)

    # Ordenamiento de datos para facilitar el uso de métodos con grupos
    datos_a_corregir.sort_values(by = ['AM','TEXTO_COMPARACION', 'F_CREATE', 'INDICE'], inplace=True)
    
    # Diccionarios utilitarios, ayudarán más adelante a dar formato a ciertos datos
    textos_comparacion_únicos = \
        datos_a_corregir['AM-TEXTO_COMPARACION'].unique()
        
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
        datos_a_corregir[['AM-TEXTO_COMPARACION']].replace(
            to_replace=textos_comparacion_idx_dicc,
        )
        
    # Reordenamiento de columnas
    datos_a_corregir = \
        datos_a_corregir[
            [
                'AM',
                'AM-C_EVENTO',
                'TEXTO_COMPARACION',
                'C_EVENTO', 
                'D_EVENTO',
                'SIMILITUD',
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
                    'QID',
                ],
            keep='first',
        )
    
    datos_a_corregir['RANK'] = datos_a_corregir.groupby("QID")["EVALUACION"].rank('first', ascending =  False)
    datos_a_corregir.loc[datos_a_corregir['RANK'] > 10, 'RANK'] = 11
    
    datos_a_corregir = datos_a_corregir.sort_values(["QID","RANK"])
    datos_a_corregir = datos_a_corregir.reset_index()
    datos_a_corregir["INDEX"] = datos_a_corregir.index
    datos_a_corregir.drop('index', axis=1, inplace=True)
    
    return datos_a_corregir

def vectorizing_data(
    datos_a_procesar: pd.DataFrame,
    model_w2v: model_w2v,
    pdt: ProcesadorDeTexto(),
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

        
    return datos_a_procesar

