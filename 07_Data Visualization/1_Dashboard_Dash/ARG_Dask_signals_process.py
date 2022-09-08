# -*- coding: utf-8 -*-
"""
Procesos y dataframes outputs de análisis señales.
"""

import pandas as pd
import numpy as np
import dask
import dask.dataframe as dd

import matplotlib.pyplot as plt
import seaborn as sns

from utils import funciones_formato

#1. Lectura de datos (Datos dask de prueba)

#1.0 - Señales a analizar
df_signals = dd.read_parquet('abfs://desarrollo-data/date=20220820/', 
                         storage_options={"account_name": "predlsandbox",
                                          "account_key": "5qMzmvlaPbb605ZTuFrq4pe7N29vjj2Ful0tWDE9i0l0hIL5qguRNFxJ1AblwiemHUKdZkS8AfysgcRGcWsd2w=="},
                         columns =  ["Time",
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
                                     "hsa12_group_hsasegid_C1075052607"])

df_signals = funciones_formato.format_(df_signals).compute()

#1.1 - Muestra ideal Mayo 2022
df_mayo = pd.read_csv("C:/Users/cflorelu/Documents/DSVM/data_extra/202205_ccd2_iba_ideal.csv")

df_mayo["llave_comparativa"] = df_mayo["signal"] + " | " + \
                               df_mayo["Grado"].astype(str) + " | " + \
                               df_mayo["Velocidad"].astype(str) + " | " + \
                               df_mayo["Ancho"].astype(str)

df_mayo = df_mayo.loc[:,["llave_comparativa",'Avg', 'Stddev', 'Min', 'Max', 'Q1', 'Q2', 'Q3', 'Count']].sort_values("Count", ascending = False)

df_mayo['Avg'] = df_mayo['Avg'].astype(float)
df_mayo['Stddev'] = df_mayo['Stddev'].astype(float)
df_mayo['Min'] = df_mayo['Min'].astype(float)
df_mayo['Max'] = df_mayo['Max'].astype(float)
df_mayo['Q1'] = df_mayo['Q1'].astype(float)
df_mayo['Q3']= df_mayo['Q3'].astype(float)
df_mayo['Count'] = df_mayo['Count']

df_mayo["iqr"] = df_mayo["Q3"] - df_mayo["Q1"]
df_mayo["outlierDown"] = df_mayo["Q1"] - (1.5 * df_mayo["iqr"])
df_mayo["outlierUp"] = df_mayo["Q3"] + (1.5 * df_mayo["iqr"])

#############
#2. Análisis#
#############

## -- 2.1 - Creación de un rango para Outliers (Comparativo muestra ideal Mayo 2022) -- ##
df_day = pd.melt(df_signals,
                 id_vars=["Time",'grado_acero', 'velocidad_linea','ancho_slab'],
                 value_vars=df_signals.columns[1:])

df_day["llave_comparativa"] = df_day["variable"] + " | " + \
                              df_day["grado_acero"].astype(str) + " | " + \
                              df_day["velocidad_linea"].astype(str) + " | " + \
                              df_day["ancho_slab"].astype(str)

df_day = df_day.loc[:,['llave_comparativa','Time','value']]

df_day = df_day.merge(df_mayo, on='llave_comparativa', how = 'left')
df_day = df_day[~df_day["Avg"].isnull()]

df_day["status_outlier"] = 'estable'

df_day.loc[df_day["value"] >= df_day["outlierUp"], "status_outlier"] = 'outlierUp'
df_day.loc[df_day["value"] <= df_day["outlierDown"],"status_outlier"] = 'outlierDown'

df_outlier = df_day.groupby(["llave_comparativa","status_outlier"]).count().iloc[:,0]
df_tmp = df_outlier.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum())).reset_index().sort_values("llave_comparativa", ascending= False)

df_outlier = df_tmp["llave_comparativa"].str.split("|",expand=True)
df_outlier["dia"] = '2022-08-20'
df_outlier["status_outlier"] = df_tmp["status_outlier"]
df_outlier["pct_comparativo_mayo22"] = df_tmp["Time"]

df_outlier.columns = ["señal","grado_acero","velocidad_linea","ancho_slab","dia","status_outlier","pct_comparativo_mayo22"]
df_outlier = df_outlier[df_outlier["pct_comparativo_mayo22"] != 100]

## -- 2.2 - Completitud de la información (Porcentaje de valores Null, 0 y distintos de 0) -- ##

df_time = funciones_formato.seconds_day(day_gregorate = '2022-08-20').compute()

df_complete = dd.merge(df_time,
                       df_signals,
                       on='Time',
                       how='left').compute()

df_zero = funciones_formato.missing_groups(df_complete, value = 'zero').compute()
df_no_zero = funciones_formato.missing_groups(df_complete, value = 'no_zero').compute()
df_null = funciones_formato.missing_groups(df_complete, value = 'null').compute()

df_missing_groups = pd.merge(df_no_zero, df_zero, on = 'signals', how = 'outer')
df_missing_groups = pd.merge(df_missing_groups, df_null, on = "signals", how = 'outer')
df_missing_groups = df_missing_groups.fillna(0)

df_missing_groups["validacion"] =  df_missing_groups["pct_val_zero"] + df_missing_groups["pct_val_no_zero"] + df_missing_groups["pct_val_null"]
df_missing_groups = df_missing_groups.loc[:,['day_x','signals','pct_val_no_zero','pct_val_zero','pct_val_null', 'validacion']]
df_missing_groups = df_missing_groups.sort_values("pct_val_zero", ascending = False)

df_missing_groups_example = df_missing_groups[df_missing_groups["signals"] == "hsa12_loopout_dslsprtrdactrod_C1075052647"]

## -- 2.3 Box Plot diario -- ##

signal_box = 'hsa12_loopout_dslsprtrdactrod_C1075052647 | 7026.0 | 1.0 | 1200-1400'
df_day["hora"] = df_day["Time"].dt.hour.astype(str)

df_box = df_day[df_day["llave_comparativa"] == signal_box]

plt.rcParams["axes.titlesize"] = 15
plt.xticks(rotation=90)
plt.rcParams['figure.figsize'] = [12, 8]
left, right = plt.xlim()

df_box_range = df_mayo[df_mayo["llave_comparativa"] == signal_box]

plt.axhline(y = float(df_box_range["outlierDown"]),linewidth=2, color='r')
plt.axhline(y = float(df_box_range["outlierUp"]),linewidth=2, color='r')
plt.subplots_adjust(bottom=0.20)

fig = sns.boxplot(x = "hora",
                  y = "value",
                  data = df_box).set(title = f'{signal_box}, señal | grado | velocidad | ancho')

df_box = df_outlier[df_outlier["señal"].str.contains('hsa12_loopout_dslsprtrdactrod_C1075052647')] 
df_box = df_box.loc[:,['señal', 'grado_acero', 'velocidad_linea', 'ancho_slab',
              'status_outlier', 'pct_comparativo_mayo22']]

#####################
## 3. Bases Output ##
#####################

df_day.to_csv("df_day.csv") #Señal con sus valores descriptivos de la muestra ideal

df_missing_groups.to_csv("df_missing_groups.csv") #Indicador de valores faltantes

df_outlier.to_csv("df_outlier.csv") #Indicador de valores outlier

####################
## 4. Dash Plotly ##  
####################

















