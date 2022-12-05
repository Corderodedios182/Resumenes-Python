# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 06:26:00 2022

@author: cflorelu
"""
from settings import *

def training(
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