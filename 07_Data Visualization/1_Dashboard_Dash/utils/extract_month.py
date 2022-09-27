# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 10:54:36 2022

@author: cflorelu
"""
import datetime
from datetime import datetime, timedelta
from utils import transformations
from utils import values
import dask.dataframe as dd
import pandas as pd

def date_range_to_be_extracted(day_gregorate = datetime.today()):
    
    day_gregorate_start = datetime.today() + timedelta(days =-5)
    day_gregorate_end = datetime.today()
    
    yr = day_gregorate_start.year
    mnth = day_gregorate_start.month
    start_day = day_gregorate_start.day
    end_day = day_gregorate_end.day
    
    from_time = '{0}-{1}-{2}'.format(yr, mnth, start_day)
    end_time  = '{0}-{1}-{2}'.format(yr, mnth, end_day)
    
    fecha = lambda x: int(x.strftime("%Y-%m-%d").replace("-",""))
    
    init_flt = datetime.strptime(from_time, "%Y-%m-%d")
    end_flt = datetime.strptime(end_time, "%Y-%m-%d")
    
    date_range = [fecha(x) for x in pd.date_range(start=init_flt,end=end_flt).to_pydatetime().tolist()]
    
    return date_range

def azure_data_extraction():

    ddf_list = []
    date_range = date_range_to_be_extracted()
    
    for i in date_range:
        
        ddf_signal = dd.read_parquet(f'abfs://arg-landing-iba-sns-ccd2@prodllanding.blob.core.windows.net/date={i}/*.parquet',
                                        storage_options = {"account_name": values.config_values['Signals']['account_name'],
                                                           "sas_token": values.config_values['Signals']['sas_token']},
                                        blocksize = None,
                                        columns = values.config_values['Signals']['columns_file'])
        
        ddf_signal = transformations.format_groups(ddf_signal).compute()
        
        ddf_list.append(ddf_signal) 
    
    ddf_signal = pd.concat(ddf_list)
    
    return ddf_signal
    
azure_data_extraction().to_csv("data/ddf_signal.csv", index=False)
