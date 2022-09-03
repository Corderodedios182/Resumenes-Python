# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 11:56:10 2022

@author: cflorelu
"""

import dask
import pandas as pd
import numpy as np

@dask.delayed
def format_(df):
    """Formato a las señales extraidas.
       Agrupa por segundo para disminuir los datos de milisegundos a segundos.
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
    df["ancho_slab"] = df["ancho_slab"].astype(str)

    df["velocidad_linea"] = df[velocidad_linea].apply(lambda x: round(x, 1))
    df["velocidad_linea"] = df["velocidad_linea"].astype(str)

    df["grado_acero"] = df[grado_acero]
    df["grado_acero"] = df["grado_acero"].astype(str)
    
    df = df.drop([ancho_slab, velocidad_linea, grado_acero], axis = 1)

    return df

