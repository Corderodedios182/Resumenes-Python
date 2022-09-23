# -*- coding: utf-8 -*-
"""
Procesos y dataframes outputs de análisis señales.
"""

#Data Processing
import dask.dataframe as dd
import pandas as pd

import plotly.io as pio
pio.renderers.default='browser'

#utils
from utils import values 
from utils import transformations

#Load data Azure
day_gregorate = '2022-09-02'
day_files = '20220902'

ddf_signal = dd.read_parquet(f'abfs://arg-landing-iba-sns-ccd2@prodllanding.blob.core.windows.net/date={day_files}',
                      storage_options = {"account_name": values.config_values['Signals']['account_name'],
                                         "sas_token": values.config_values['Signals']['sas_token']},
                      blocksize = None,
                      columns = values.config_values['Signals']['columns_file'])

ddf_may = dd.read_csv('abfs://mtto-predictivo-input-arg@prodltransient.blob.core.windows.net/202205_ccd2_iba_ideal.csv',
                       storage_options = {"account_name": values.config_values['May22']['account_name'],
                                         "sas_token": values.config_values['May22']['sas_token']},
                       blocksize = None).compute()
#Transformations
ddf_signal = transformations.format_groups(ddf_signal).compute()

ddf_signal = pd.read_csv("data/ddf_signal.csv")

#Status_completitud (Para todas la señales)
ddf_time = transformations.seconds_day(day_gregorate).compute()
ddf_missing_groups = transformations.group_completeness(ddf_time, ddf_signal)

#Muestra ideal Mayo 2022
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
                       value_vars = ddf_complete.columns[1:])

ddf_complete["groupings"] = ddf_complete["groupings"].fillna("no_group")
ddf_complete["value"] = ddf_complete["value"].fillna(.99)

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

ddf_may_tmp = ddf_may[ddf_may["signal_may22"].str.contains("hsa12_loopout_dslsprtrdactpst_C1075052646")]
ddf_complete_tmp = ddf_complete[ddf_complete["variable"] == 'hsa12_loopout_dslsprtrdactpst_C1075052646']

ddf_complete = ddf_complete.merge(ddf_may,
                                  left_on ='key_group',
                                  right_on = 'key_group_may22',
                                  how = 'left')

found_may = ddf_complete[~ddf_complete["Avg_may22"].isnull()]["key_group"].unique()
no_found_may = ddf_complete[ddf_complete["Avg_may22"].isnull()]["key_group"].unique()

ddf_complete = ddf_complete[~ddf_complete["Avg_may22"].isnull()]

ddf_complete["outlier_status"] = 'within_range'

ddf_complete.loc[ddf_complete["value"] >= ddf_complete["outlierUp_may22"], "outlier_status"] = 'out_upper_range'
ddf_complete.loc[ddf_complete["value"] <= ddf_complete["outlierDown_may22"],"outlier_status"] = 'out_lower_range'

df_outlier = ddf_complete.groupby(["key_group","outlier_status"]).count().iloc[:,0]

df_outlier = df_outlier.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum())).reset_index().sort_values("key_group", ascending= False)

df_outlier.columns = ["key_group","outlier_status","pct_outlier_comparative_mayo22"]
df_outlier = df_outlier[df_outlier["pct_outlier_comparative_mayo22"] != 100]

df_outlier = df_outlier.pivot(index = "key_group",
                              columns = 'outlier_status',
                              values = "pct_outlier_comparative_mayo22").fillna(0).reset_index()

df_outlier["sum_validation_ouliter_ranges"] = df_outlier["within_range"] + df_outlier["out_lower_range"] + df_outlier["out_upper_range"]

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
                        	"out_upper_range","sum_validation_ouliter_ranges","indicator"]]

df_dash = df_ideal.loc[:,["country",'day', 'key_group','signal','pct_val_no_zeros', 'within_range', 'Cantidad_CU_may22','indicator']]

#No mandar con index
#Formato redondeado de números a un digito
df_ideal.to_csv("data/df_ideal.csv")
df_ideal.to_csv("data/df_dash.csv")
comparative_sample.to_csv("data/df_comparative_sample.csv")

#Cruze y outliers

#fig = px.scatter(
#    ddf_complete_tmp,
#    x = "Time",
#    y = "value", 
#    color = "groupings",
#    title = "Detalle de grupos por señal grado acero | velocidad linea | ancho planchon")

#fig.show()
