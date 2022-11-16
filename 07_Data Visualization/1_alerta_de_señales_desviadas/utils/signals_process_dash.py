# -*- coding: utf-8 -*-
"""
Procesos y dataframes outputs de análisis señales.
"""
#Data Processing
import dask.dataframe as dd
import pandas as pd
import os

#utils
from utils import values 
from utils import transformations
from utils import extract_month_azure

#Datos comparativos
if "ddf_may.csv" in os.listdir("data/ddf_dash"):
    ddf_may = dd.read_csv("data/ddf_dash/ddf_may.csv").compute().round(1)
else:
    ddf_may = dd.read_csv('abfs://mtto-predictivo-input-arg@prodltransient.blob.core.windows.net/202205_ccd2_iba_ideal.csv',
                           storage_options = {"account_name": values.config_values['May22']['account_name'],
                                             "sas_token": values.config_values['May22']['sas_token']},
                           blocksize = None).compute()
    ddf_may.to_csv("data/ddf_dash/ddf_may.csv").round(1)

#Datos señales
status_extraction = extract_month_azure.azure_data_extraction(day_gregorate = '2022-11-14', days = 2)

if status_extraction == 'No se descargaron archivos de azure':
   ddf_signal = dd.read_csv("data/ddf_signal/*.csv").compute()
else:
   extract_month_azure.azure_data_extraction()
   ddf_signal = dd.read_csv("data/ddf_signal/*.csv").compute()

ddf_signal['Time'] = pd.to_datetime(ddf_signal['Time'])

#--Prueba de una señal (Comentar si no se está debuggeando)
#ddf_may = ddf_may[ddf_may["signal"].str.contains("hsa12_group_hsarefgauts_C1075052603")]
#ddf_signal = ddf_signal.loc[:, ['Time','groupings',"hsa12_group_hsarefgauts_C1075052603"]]

#--- Status_completitud (Para todas la señales)
ddf_time = transformations.seconds_day(min(ddf_signal['Time'].dt.floor("D")),
                                       max(ddf_signal['Time'].dt.floor("D"))).compute()

ddf_missing_groups = transformations.group_completeness(ddf_time,
                                                        ddf_signal)

#--- Muestra ideal Mayo 2022
ddf_may["Grado"] = ddf_may["Grado"].astype(int)
ddf_may["Velocidad"] = ddf_may["Velocidad"].apply(lambda x: round(x, 1))

ddf_may["key_group"] = ddf_may["signal"].astype(str) + " | " + \
                       ddf_may["Grado"].astype(str) + " | " + \
                       ddf_may["Velocidad"].astype(str) + " | " + \
                       ddf_may["Ancho"].astype(str)

ddf_may["iqr"] = ddf_may["Q3"] - ddf_may["Q1"]
ddf_may["outlierDown"] = ddf_may["Q1"] - (1.5 * ddf_may["iqr"])
ddf_may["outlierUp"] = ddf_may["Q3"] + (1.5 * ddf_may["iqr"])
ddf_may.columns = ddf_may.columns + "_may22"

#status_outlier y status_cu
ddf_complete = dd.merge(ddf_time,
                        ddf_signal,
                        on='Time',
                        how='left').compute()

ddf_complete = pd.melt(ddf_complete,
                       id_vars = ["Time","second_day",'groupings'],
                       value_vars = ddf_complete.columns[2:-4])

ddf_complete["groupings"] = ddf_complete["groupings"].fillna("no_group")
ddf_complete["value"] = ddf_complete["value"].fillna(0)
ddf_complete["value"] = round(ddf_complete["value"],1)

ddf_complete["key_group"] = ddf_complete["variable"] + " | " + \
                            ddf_complete["groupings"].astype(str)

#¿Cuantos grupos se encuentran en las muestras ideales de mayo 2022?
keys_group_may22     = ddf_may["key_group_may22"].unique()
keys_group_analyisis = ddf_complete["key_group"].unique()
found = [item in list(keys_group_analyisis) for item in list(keys_group_may22)]

comparative_sample = {"n_signals_may22"     : len(ddf_may["signal_may22"].unique()),
                      "n_signal_analysis"   : len(ddf_complete["variable"].unique()),
                      "n_groupings_may22"   : len(keys_group_may22),
                      "n_groupings_analysis": len(keys_group_analyisis),
                      "groups_found"        : sum(found),
                      "groups_not_found"    : keys_group_analyisis.shape[0] - sum(found)
                      }

comparative_sample = pd.DataFrame(list(comparative_sample.items()),
                                  columns = ['feature','number'])

ddf_complete = ddf_complete.merge(ddf_may,
                                  left_on ='key_group',
                                  right_on = 'key_group_may22',
                                  how = 'left')

found_may = ddf_complete[~ddf_complete["Avg_may22"].isnull()]["key_group"].unique()
no_found_may = ddf_complete[ddf_complete["Avg_may22"].isnull()]["key_group"].unique()

ddf_complete

ddf_complete = ddf_complete[~ddf_complete["Avg_may22"].isnull()]

ddf_complete["outlier_status"] = 'within_range'

ddf_complete.loc[ddf_complete["value"] > ddf_complete["outlierUp_may22"], "outlier_status"] = 'out_upper_range'
ddf_complete.loc[ddf_complete["value"] < ddf_complete["outlierDown_may22"],"outlier_status"] = 'out_lower_range'

df_outlier = ddf_complete.groupby(["key_group","outlier_status"]).count().iloc[:,0]

df_outlier = df_outlier.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum())).reset_index().sort_values("key_group", ascending= False)

df_outlier.columns = ["key_group","outlier_status","pct_outlier_comparative_mayo22"]

df_outlier = df_outlier.pivot(index = "key_group",
                              columns = 'outlier_status',
                              values = "pct_outlier_comparative_mayo22").fillna(0).reset_index()

df_outlier = df_outlier.merge(ddf_may,
                              left_on='key_group',
                              right_on='key_group_may22',
                              how = 'inner')

#Todo junto.
df_ideal = df_outlier.merge(ddf_missing_groups,
                            left_on = 'signal_may22',
                            right_on='signal',
                            how = 'inner')

df_ideal["indicator"] = "revision"
df_ideal.loc[(df_ideal["pct_val_no_zeros"] >= .60) & ((df_ideal["within_range"] >= 60)), "indicator"] = "media"
df_ideal.loc[(df_ideal["pct_val_no_zeros"] >= .80) & ((df_ideal["within_range"] >= 80)), "indicator"] = "estable"
df_ideal.loc[df_ideal["Cantidad_CU_may22"] == 0, "Cantidad_CU_may22"] = 1
df_ideal["country"] = "Argentina"

df_ideal = df_ideal.loc[:,["country", "day", "signal","Grado_may22","Velocidad_may22","Ancho_may22","key_group","Count_may22","Avg_may22","Stddev_may22",
                     	   "Min_may22","Max_may22","Q1_may22","Q2_may22","Q3_may22","iqr_may22","outlierDown_may22","outlierUp_may22","Cantidad_CU_may22",
                        	"pct_val_no_zeros","pct_val_equal_zero","pct_val_null","sum_validation_completeness","within_range","out_lower_range",
                        	"out_upper_range","indicator"]]

df_dash = df_ideal.loc[:,["country",'day', 'key_group','signal','pct_val_no_zeros', 'within_range', 'Cantidad_CU_may22','indicator']]

df_ideal.to_csv("data/ddf_dash/df_ideal.csv", index=False)
df_dash.to_csv("data/ddf_dash/df_dash.csv", index=False)
comparative_sample.to_csv("data/ddf_dash/df_comparative_sample.csv", index=False)
