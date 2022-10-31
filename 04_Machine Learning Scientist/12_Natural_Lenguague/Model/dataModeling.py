# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 06:11:38 2022

@author: cflorelu
"""
from settings import *

## -División de datos - Exploración y Prueba
def split_data(
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
        datos_entrna.loc[:, ~datos_entrna.columns.isin(['rank'])]
    y_entrna = \
        datos_entrna.loc[:,  datos_entrna.columns.isin(['rank'])]
    x_valida = \
        datos_valida.loc[:, ~datos_valida.columns.isin(['rank'])]
    y_valida = \
        datos_valida.loc[:,  datos_valida.columns.isin(['rank'])]
    x_prueba = \
        datos_prueba.loc[:, ~datos_prueba.columns.isin(['rank'])]
    y_prueba = \
        datos_prueba.loc[:,  datos_prueba.columns.isin(['rank'])]
    
    return x_entrna, y_entrna, x_valida, y_valida, x_prueba, y_prueba

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
    
    etiquetas = y['rank']
    qids = X['QID']
    
    return caracts, etiquetas, qids
