# -*- coding: utf-8 -*-
"""
Funciones de procesamiento de datos para las señales
"""

import dask
import pandas as pd
import numpy as np
import dask.dataframe as dd

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

@dask.delayed
def seconds_day(min_day_gregorate, max_day_gregorate):
    """Dataframe con los 84,000 segundos del día"""
    
    df_time = pd.DataFrame(dict(Time = pd.Series(pd.date_range(start = min_day_gregorate,
                                                               end = max_day_gregorate,
                                                               freq = 's'))))

    df_time["second_day"] = df_time.index
    df_time = dd.from_pandas(df_time, npartitions = 1)
    
    return df_time

@dask.delayed
def missing_groups(ddf_complete,
                   value= 'zero'):
    """Dataframe con los diferentes porcentajes de valores faltantes en señales"""

    def percentage_zero(ddf_complete, value = value):
        
        if (value == 'zero'):
            return ((ddf_complete == 0) & (ddf_complete.notnull())).sum(axis=0)
        elif (value == 'no_zero'):
            return ((ddf_complete != 0) & (ddf_complete.notnull())).sum(axis=0)
        else:
            return ddf_complete.isnull().sum(axis=0)
    
    if (value == 'zero'):
        pct_val = "pct_val_equal_zero"
    elif (value == 'no_zero'):
        pct_val = "pct_val_no_zeros"
    else:
        pct_val = "pct_val_null"
        
    ddf_complete["day"] = ddf_complete['Time'].dt.floor("D")
    ddf_complete = ddf_complete.groupby(["day"]).apply(percentage_zero)
    ddf_complete = (ddf_complete/86400) * 100
    ddf_complete = ddf_complete.drop(['Time', 'second_day', 'day'], axis =1)
    ddf_complete = ddf_complete.transpose().reset_index()
    ddf_complete = pd.melt(ddf_complete, id_vars=["index"], value_vars = ddf_complete.columns[1:])
    
    ddf_complete.columns = ["signals","day",pct_val]
    ddf_complete = ddf_complete[ddf_complete[pct_val] > 0]
    ddf_complete = ddf_complete.sort_values(by = pct_val, ascending = False)
    ddf_complete["key"] = ddf_complete["signals"].astype(str) + "_" + ddf_complete["day"].astype(str)
    
    return ddf_complete

def group_completeness(ddf_time,
                       ddf_signal):
    
    ddf_complete = dd.merge(ddf_time,
                            ddf_signal.iloc[:,:-1],
                            on='Time',
                            how='left').compute()

    ddf_zero    = missing_groups(ddf_complete, value = 'zero').compute()
    ddf_no_zero = missing_groups(ddf_complete, value = 'no_zero').compute()
    ddf_null    = missing_groups(ddf_complete, value = 'null').compute()

    ddf_missing_groups = pd.merge(ddf_no_zero, ddf_zero, on = 'key', how = 'outer')
    ddf_missing_groups["day_x"] = ddf_missing_groups["day_x"].fillna(ddf_missing_groups["day_y"])
    ddf_missing_groups["signals_x"] = ddf_missing_groups["signals_x"].fillna(ddf_missing_groups["signals_y"])
    
    ddf_missing_groups = pd.merge(ddf_missing_groups, ddf_null, on = "key", how = 'outer')
    ddf_missing_groups["day_x"] = ddf_missing_groups["day_x"].fillna(ddf_missing_groups["day"])
    ddf_missing_groups["signals_x"] = ddf_missing_groups["signals_x"].fillna(ddf_missing_groups["signals"])
    
    ddf_missing_groups = ddf_missing_groups.fillna(0)
    ddf_missing_groups["sum_validation_completeness"] =  ddf_missing_groups["pct_val_equal_zero"] + ddf_missing_groups["pct_val_no_zeros"] + ddf_missing_groups["pct_val_null"]
    ddf_missing_groups = ddf_missing_groups.loc[:,['day_x','signals_x','pct_val_no_zeros','pct_val_equal_zero','pct_val_null', 'sum_validation_completeness']]
    ddf_missing_groups = ddf_missing_groups.sort_values("pct_val_equal_zero", ascending = False)
    ddf_missing_groups.columns = ["day","signal",'pct_val_no_zeros','pct_val_equal_zero','pct_val_null', 'sum_validation_completeness']
    ddf_missing_groups = ddf_missing_groups.sort_values(["signal","day"], ascending = True)

    return ddf_missing_groups


