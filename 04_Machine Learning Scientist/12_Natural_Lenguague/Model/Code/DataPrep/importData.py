# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 12:58:21 2022

@author: cflorelu
"""
from settings import *

def read_data(
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

def read_data_test():
      
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, "raw/data_repoblada/*.csv"))
        
    main_dataframe = pd.DataFrame(pd.read_csv(csv_files[0]))
      
    for i in range(1,len(csv_files)):
        data = pd.read_csv(csv_files[i], sep = ',')
        df = pd.DataFrame(data)
        main_dataframe = pd.concat([main_dataframe, df], axis = 0)
      
    return main_dataframe
        