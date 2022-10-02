# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 10:54:36 2022

@author: cflorelu
"""
import os
import re
import datetime

from datetime import datetime, timedelta
from utils import transformations
from utils import values
import dask.dataframe as dd
import pandas as pd

def date_range_to_be_extracted(day_gregorate = datetime.today()):
    """
    Parameters
    ----------
    day_gregorate : TYPE, optional
        DESCRIPTION. The default is datetime.today().

    Returns
    -------
    date_range : TYPE
        Listado de fechas para lectura de datos ejemplo :
            
            [20220927, 20220928, 20220929, 20220930, 20221002]

    """
    
    day_gregorate_start = datetime.today() + timedelta(days =-3)
    day_gregorate_end = datetime.today()
    
    yr_start = day_gregorate_start.year
    mnth_start = day_gregorate_start.month
    start_day = day_gregorate_start.day
    
    yr_end = day_gregorate_end.year
    mnth_end = day_gregorate_end.month
    end_day = day_gregorate_end.day
    
    from_time = '{0}-{1}-{2}'.format(yr_start, mnth_start, start_day)
    end_time  = '{0}-{1}-{2}'.format(yr_end, mnth_end, end_day)
    
    fecha = lambda x: int(x.strftime("%Y-%m-%d").replace("-",""))
    
    init_flt = datetime.strptime(from_time, "%Y-%m-%d")
    end_flt = datetime.strptime(end_time, "%Y-%m-%d")
    
    date_range = [fecha(x) for x in pd.date_range(start=init_flt,end=end_flt).to_pydatetime().tolist()]
    
    return date_range

def azure_data_extraction():
    """
    Returns
    -------
    TYPE
        Valida los archivos existentes en : data/ddf_signal
            
        Para lectura en caso de que no existan los descarga de Azure.
    """
    
    date_range = date_range_to_be_extracted()
    
    extract_number = lambda x : int(re.findall(r'\d+', x)[0])
    files_exist = [extract_number(x) for x in os.listdir("data/ddf_signal")]
    
    missing_files = [item in list(files_exist) for item in list(date_range)]
    
    date_range = pd.DataFrame({"date_range": date_range,
                               "faltantes": missing_files})
    
    date_range = list(date_range[date_range["faltantes"].isin([False])]["date_range"])
    
    for i in date_range:
        
        ddf_signal = dd.read_parquet(f'abfs://arg-landing-iba-sns-ccd2@prodllanding.blob.core.windows.net/date={i}/*.parquet',
                                        storage_options = {"account_name": values.config_values['Signals']['account_name'],
                                                           "sas_token": values.config_values['Signals']['sas_token']},
                                        blocksize = None,
                                        columns = values.config_values['Signals']['columns_file'])
        
        ddf_signal = transformations.format_groups(ddf_signal).compute()
        
        ddf_signal.to_csv(r"data/ddf_signal/ddf_signal_{day}.csv".format(day = i), index=False)
        
    return print("Archivo: ", r"ddf_signal_{day}.csv".format(day = i), "guardado")
