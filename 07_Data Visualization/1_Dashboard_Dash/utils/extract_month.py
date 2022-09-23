# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 10:54:36 2022

@author: cflorelu
"""

import dask
import dask.dataframe as dd
import pandas as pd
import numpy as np

#################
#Valores Filtros#
#################
signals = ["Time",
           "s4_an2l_ramactwidthboc_C1611", #ancho plataforma
           "s4_hmo_pmac_fmplc_m5043_an2l_hmo_castspeed_C0470", #velodicdad línea
           "grade_number_C1074659440", #grado_acero
           "s4_drv_net_a_ea_seg12_torque_reff_C1074856029", #señales de línea 4 y segmento 12
           "s4_drv_net_a_ea_seg12_torque_ref_C1074856020",
           "hsa12_loopout_eslsprtrdactpst_C1075052642",
           "hsa12_loopout_esrsprtrdactpst_C1075052644",
           "hsa12_loopout_eslsprtrdactrod_C1075052643",
           "hsa12_loopout_esrsprtrdactrod_C1075052645",
           "hsa12_loopout_dslsprtrdactpst_C1075052646",
           "hsa12_loopout_dsrsprtrdactpst_C1075052648",
           "hsa12_loopout_dslsprtrdactrod_C1075052647",
           "hsa12_loopout_dsrsprtrdactrod_C1075052649",
           "hsa12_loopout_eslsactfrc_C1075052638",
           "hsa12_loopout_esrsactfrc_C1075052639",
           "hsa12_loopout_dslsactfrc_C1075052640",
           "hsa12_loopout_dsrsactfrc_C1075052641",
           "hsa12_group_hsaactgauts_C1075052605",
           "hsa12_group_hsaactgaubs_C1075052606",
           "hsa12_group_hsarefgaubs_C1075052604",
           "hsa12_group_hsarefgauts_C1075052603",
           "hsa12_loopout_dslsactpos_C1075052636",
           "hsa12_loopout_dsrsactpos_C1075052637",
           "hsa12_loopout_eslsactpos_C1075052634",
           "hsa12_loopout_esrsactpos_C1075052635",
           "s4_drv_net_a_ea_seg12_linear_speed_C1074856027",
           "s4_drv_net_a_ea_seg012_trq_cmd_C1611726945",
           "s4_drv_net_a_ea_seg12_actual_current_C1074856026",
           "s4_drv_net_a_ea_seg12_speed_ref_C1074856019",
           "hsa12_group_hsasegid_C1075052607"]

day_gregorate = '2022-09-02'
day_files = ['20220923','20220922','20220921']

###############
#Valores Azure#
###############
config_values = {'Signals': {
                    'account_name': 'prodllanding',
                    'sas_token': 'sp=rl&st=2022-04-05T18:14:27Z&se=2023-01-01T03:14:27Z&sv=2020-08-04&sr=c&sig=%2Fqe%2F4HbbTL6Tvx2oYNkF2tV7Qjjdj%2BsO2fDdldVinUU%3D', 
                    'source': 'abfs://arg-landing-iba-sns-ccd2@prodllanding.blob.core.windows.net/date={date_}',
                    'columns_file': signals,
                    'columns_order': signals,
                    'columns_to_date': ['Time'],
                    'skip_rows': 0,
                    'output_ddf': 'ddf'
                    },
                'May22': {
                    'account_name': 'prodltransient',
                    'sas_token': 'sp=racwdli&st=2022-09-19T17:56:44Z&se=2023-07-30T01:56:44Z&sv=2021-06-08&sr=c&sig=doxPebIqOWxap%2BaZlvgsCqcEw51f7D2Jf26ObC%2FCSSQ%3D',
                    'source': 'abfs://mtto-predictivo-input-arg@prodltransient.blob.core.windows.net/202205_ccd2_iba_ideal.csv',
                    'columns_file': '',
                    'columns_new': '',
                    'columns_to_date': ['Time'],
                    'skip_rows': 0,
                    'output_ddf': 'ddf_may'}
                }

################
#Conexión Azure#
################
import datetime

yr = 2021
mnth = 1
start_day = 1 
end_day = 2
signals = ["s4_drv_net_a_ea_seg04t_torque_reff_filt__C1117"]
level   = ["year"]
from_time = '{0}-{1}-{2} 00:00:00'.format(yr, mnth, start_day)
end_time  = '{0}-{1}-{2} 00:00:00'.format(yr, mnth, end_day)
formato_sampling = "yyyy-MM-dd"
fecha = lambda x: x.strftime("%Y-%m-%d").replace("-","")
init_flt = datetime.datetime.strptime(from_time, "%Y-%m-%d %H:%M:%S")
end_flt = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
date_range = [fecha(x) for x in pd.date_range(start=init_flt,end=end_flt).to_pydatetime().tolist()]
line = "ccd2" #"laca" "ccd2" (laca, molino caliente / Carter 2)
container = "arg-landing-iba-sns-"+line
account = "prodllanding"
complete_dir = ''
time_variable = "Time"
ranges = 'date={'+','.join(date_range)+'}/*.parquet'
dir_url = 'wasbs://' + container + '@' + account + '.blob.core.windows.net/' + complete_dir + ranges

ddf_list = []

#Transformaciones#
@dask.delayed
def format_groups(df):
    """Formato a las señales extraidas.
       Agrupa por segundo para disminuir los datos de milisegundos a segundos.
       Crea etiquetas y grupos de ancho, velocidad y grado de acero.
    """
    df['Time'] = df["Time"].dt.year.astype(str)  +"-" + \
                 df["Time"].dt.month.astype(str) +"-" + \
                 df["Time"].dt.day.astype(str)   +" " + \
                 df["Time"].dt.hour.astype(str)  +":" + \
                 df["Time"].dt.minute.astype(str)+":" + \
                 df["Time"].dt.second.astype(str)
    
    df['Time'] = pd.to_datetime(df['Time'])
    df = df.groupby(["Time"]).mean().reset_index()
    
    ancho_slab = "s4_an2l_ramactwidthboc_C1611"
    velocidad_linea = "s4_hmo_pmac_fmplc_m5043_an2l_hmo_castspeed_C0470"
    grado_acero = "grade_number_C1074659440"

    filters = [(df[ancho_slab] <= 1000),
               (df[ancho_slab] > 1000) & (df[ancho_slab] <= 1200),
               (df[ancho_slab] > 1200) & (df[ancho_slab] <= 1400),
               (df[ancho_slab] > 1400) & (df[ancho_slab] <= 1600),
               (df[ancho_slab] > 1600) & (df[ancho_slab] <= 1800),
               (df[ancho_slab] > 1800)]

    values = ["Menor a 1000",
              "1000-1200",
              "1200-1400",
              "1400-1600",
              "1600-1800",
              "Fuera Rango Ancho"]

    df["ancho_slab"] = df[ancho_slab]
    df["ancho_slab"] = np.select(filters, values)

    df["velocidad_linea"] = df[velocidad_linea].apply(lambda x: round(x, 1))

    df["grado_acero"] = df[grado_acero].astype(int)
    
    df = df.drop([ancho_slab, velocidad_linea, grado_acero], axis = 1)
    
    df["groupings"] = df["grado_acero"].astype(str) + " | " + \
                      df["velocidad_linea"].astype(str) + " | " + \
                      df["ancho_slab"].astype(str)
                        
    df = df.drop(["ancho_slab", "velocidad_linea", "grado_acero"], axis = 1)

    return df

for i in [20220902,20220901,20220903,20220904,20220905]:
    
    ddf_signal = dd.read_parquet(f'abfs://arg-landing-iba-sns-ccd2@prodllanding.blob.core.windows.net/date={i}/*.parquet',
                                    storage_options = {"account_name": config_values['Signals']['account_name'],
                                                       "sas_token": config_values['Signals']['sas_token']},
                                    blocksize = None,
                                    columns = config_values['Signals']['columns_file'])
    
    ddf_signal = format_groups(ddf_signal).compute()
    
    ddf_list.append(ddf_signal) 

ddf_signal = pd.concat(ddf_list)

ddf_signal.to_csv("ddf_signal.csv")
