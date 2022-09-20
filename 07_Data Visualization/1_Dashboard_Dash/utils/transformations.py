# -*- coding: utf-8 -*-
"""
Funciones de procesamiento de datos para las señales
"""

import dask
import pandas as pd
import numpy as np
import dask.dataframe as dd

day_gregorate = '2022-09-02'

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

    df["grado_acero"] = df[grado_acero]
    
    df = df.drop([ancho_slab, velocidad_linea, grado_acero], axis = 1)
    
    df["groupings"] = df["grado_acero"].astype(str) + " | " + \
                      df["velocidad_linea"].astype(str) + " | " + \
                      df["ancho_slab"].astype(str)
                        
    df = df.drop(["ancho_slab", "velocidad_linea", "grado_acero"], axis = 1)

    return df

@dask.delayed
def seconds_day(day_gregorate = day_gregorate, periods = 86400):
    """Dataframe con los 84,000 segundos del día"""
    df_time = pd.DataFrame(dict(Time = pd.Series(pd.date_range(f'{day_gregorate} 00:00:00',
                                                               periods = periods, freq = 's'))))
    df_time["second_day"] = df_time.index
    df_time = dd.from_pandas(df_time, npartitions = 1)
    
    return df_time

@dask.delayed
def missing_groups(df,
                   value= 'zero',
                   day_gregorate = day_gregorate):

    def percentage_zero(df, value = value):
        
        if (value == 'zero'):
            return ((df == 0) & (df.notnull())).sum(axis=0)
        elif (value == 'no_zero'):
            return ((df != 0) & (df.notnull())).sum(axis=0)
        else:
            return df.isnull().sum(axis=0)
    
    if (value == 'zero'):
        pct_val = "pct_val_zero"
    elif (value == 'no_zero'):
        pct_val = "pct_val_no_zero"
    else:
        pct_val = "pct_val_null"
        
    df["day"] = df['Time'].dt.floor("D")
    df = df.groupby(["day"]).apply(percentage_zero)
    df = df/86400
    df = df.drop(['Time', 'second_day', 'day'], axis =1)
    df = df.transpose().reset_index()
    df = pd.melt(df, id_vars=["index"], value_vars=df.columns[1:])
    
    df.columns = ["signals","day",pct_val]
    df = df[df[pct_val] > 0]
    df = df.sort_values(by = pct_val, ascending = False)
    
    return df