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

#Status_completitud (Por toda la señal)
ddf_time = transformations.seconds_day(day_gregorate).compute()

ddf_complete = dd.merge(ddf_time,
                        ddf_signal.iloc[:,:-1],
                        on='Time',
                        how='left').compute()

ddf_zero = transformations.missing_groups(ddf_complete, value = 'zero').compute()
ddf_no_zero = transformations.missing_groups(ddf_complete, value = 'no_zero').compute()
ddf_null = transformations.missing_groups(ddf_complete, value = 'null').compute()

ddf_missing_groups = pd.merge(ddf_no_zero, ddf_zero, on = 'signals', how = 'outer')
ddf_missing_groups = pd.merge(ddf_missing_groups, ddf_null, on = "signals", how = 'outer')
ddf_missing_groups = ddf_missing_groups.fillna(0)

ddf_missing_groups["validacion"] =  ddf_missing_groups["pct_val_zero"] + ddf_missing_groups["pct_val_no_zero"] + ddf_missing_groups["pct_val_null"]
ddf_missing_groups = ddf_missing_groups.loc[:,['day_x','signals','pct_val_no_zero','pct_val_zero','pct_val_null', 'validacion']]
ddf_missing_groups = ddf_missing_groups.sort_values("pct_val_zero", ascending = False)
ddf_missing_groups["day_x"] = day_gregorate

ddf_missing_groups.columns = ["day","signal",'pct_val_no_zero','pct_val_zero','pct_val_null', 'validacion']

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

ddf_may_tmp = ddf_may[ddf_may["signal"].str.contains("hsa12_loopout_dslsprtrdactpst_C1075052646")]

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

#ddf_complete_tmp = ddf_complete[ddf_complete["variable"] == 'hsa12_loopout_dslsprtrdactpst_C1075052646']

#¿Cuantos grupos se encuentran en las muestras ideales de mayo 2022?
groups_may =  ddf_may_tmp["key_group"].unique()
#groups_complete_tmp = ddf_complete_tmp["key_group"].unique()
groups_complete = ddf_complete["key_group"].unique()

#encontradas = [item in groups_complete_tmp for item in groups_may]
encontradas = [item in groups_complete for item in groups_may]

#print("No se encontraron ", groups_complete_tmp.shape[0] - sum(encontradas) , " grupos de muestra para está señal")
print("No se encontraron ", groups_complete.shape[0] - sum(encontradas) , " grupos de muestra para está señal")

#ddf_complete_tmp = ddf_complete_tmp.merge(ddf_may, on='key_group', how = 'left')
ddf_complete = ddf_complete.merge(ddf_may, on='key_group', how = 'left')

#encontrados_may = ddf_complete_tmp[~ddf_complete_tmp["Avg"].isnull()]["key_group"].unique()
encontrados_may = ddf_complete[~ddf_complete["Avg"].isnull()]["key_group"].unique()

#no_encontrados_may = ddf_complete_tmp[ddf_complete_tmp["Avg"].isnull()]["key_group"].unique()
no_encontrados_may = ddf_complete[ddf_complete["Avg"].isnull()]["key_group"].unique()

#ddf_complete_tmp = ddf_complete_tmp[~ddf_complete_tmp["Avg"].isnull()]
ddf_complete = ddf_complete[~ddf_complete["Avg"].isnull()]

#ddf_complete_tmp["status_outlier"] = 'estable'
ddf_complete["status_outlier"] = 'estable'

#ddf_complete_tmp.loc[ddf_complete_tmp["value"] >= ddf_complete_tmp["outlierUp"], "status_outlier"] = 'outlierUp'
ddf_complete.loc[ddf_complete["value"] >= ddf_complete["outlierUp"], "status_outlier"] = 'outlierUp'

#ddf_complete_tmp.loc[ddf_complete_tmp["value"] <= ddf_complete_tmp["outlierDown"],"status_outlier"] = 'outlierDown'
ddf_complete.loc[ddf_complete["value"] <= ddf_complete["outlierDown"],"status_outlier"] = 'outlierDown'

#df_outlier = ddf_complete_tmp.groupby(["key_group","status_outlier"]).count().iloc[:,0]
df_outlier = ddf_complete.groupby(["key_group","status_outlier"]).count().iloc[:,0]

df_outlier = df_outlier.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum())).reset_index().sort_values("key_group", ascending= False)

df_outlier.columns = ["key_group","status_outlier","pct_comparativo_mayo22"]
df_outlier = df_outlier[df_outlier["pct_comparativo_mayo22"] != 100]

df_outlier = df_outlier.pivot(index = "key_group",
                              columns = 'status_outlier',
                              values = "pct_comparativo_mayo22").fillna(0).reset_index()

df_outlier["validacion_outlier"] = df_outlier["estable"] + df_outlier["outlierDown"] + df_outlier["outlierUp"]

df_outlier = df_outlier.merge(ddf_may, on='key_group', how = 'inner')

df_ideal = df_outlier.merge(ddf_missing_groups, on = 'signal', how = 'inner')

df_ideal.to_csv("df_ideal.csv")

df_ideal = df_ideal.loc[:,['day', 'key_group','pct_val_no_zero', 'estable', 'Cantidad_CU','signal']]

df_ideal["indicador"] = "revision"

(.20 >= .30) & (1 >=.30)

df_ideal.loc[(df_ideal["pct_val_no_zero"] >= .60) & ((df_ideal["estable"] >= 60)), "indicador"] = "media"
df_ideal.loc[(df_ideal["pct_val_no_zero"] >= .80) & ((df_ideal["estable"] >= 80)), "indicador"] = "estable"

df_ideal.loc[df_ideal["Cantidad_CU"] == 0, "Cantidad_CU"] = 1

df_ideal["pais"] = "Argentina"

df_ideal.to_csv("df_dash.csv")

#['key_group', 'estable', 'outlierDown_x', 'outlierUp_x',
# 'validacion_outlier', 'Avg', 'Stddev', 'Min', 'Max', 'Q1', 'Q2', 'Q3',
# 'Count', 'Cantidad_CU', 'signal', 'Grado', 'Velocidad', 'Ancho', 'iqr',
# 'outlierDown_y', 'outlierUp_y', , 'pct_val_no_zero',
# 'pct_val_zero', 'pct_val_null', 'validacion']

#Cruze y outliers

#fig = px.scatter(
#    ddf_complete_tmp,
#    x = "Time",
#    y = "value", 
#    color = "groupings",
#    title = "Detalle de grupos por señal grado acero | velocidad linea | ancho planchon")

#fig.show()
