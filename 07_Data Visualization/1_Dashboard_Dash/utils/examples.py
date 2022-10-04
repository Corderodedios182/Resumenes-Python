# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 12:33:09 2022

@author: cflorelu
"""
import pandas as pd
import dask.dataframe as dd

# Plotly graph objects to render graph plots
import plotly.graph_objects as go
import plotly.express as px

import plotly.io as pio
pio.renderers.default='browser'

ddf_signal = dd.read_csv("data/ddf_signal/*.csv").compute()
ddf_signal['Time'] = pd.to_datetime(ddf_signal['Time'])

ddf_signal = ddf_signal.loc[:,["Time","groupings","s4_drv_net_a_ea_seg12_linear_speed_C1074856027", "hsa12_group_hsarefgauts_C1075052603","hsa12_group_hsarefgaubs_C1075052604"]]

ddf_signal = pd.melt(ddf_signal,
                       id_vars = ["Time",'groupings'],
                       value_vars = ddf_signal.columns[2:])

fig = px.scatter(
    ddf_signal[ddf_signal["variable"] == 's4_drv_net_a_ea_seg12_linear_speed_C1074856027'],
    x="Time",
    y="value", 
    color="groupings",
    width=1600,
    height=700,
    title="Grupos generados por señal : s4_drv_net_a_ea_seg12_linear_speed_C1074856027")

fig.show()

fig = px.scatter(
    ddf_signal[ddf_signal["variable"] == 'hsa12_group_hsarefgauts_C1075052603'],
    x="Time",
    y="value", 
    color="groupings",
    width=1600,
    height=700,
    title="Grupos generados por señal : hsa12_group_hsarefgauts_C1075052603")

fig.show()

fig = px.scatter(
    ddf_signal[ddf_signal["variable"] == 'hsa12_group_hsarefgaubs_C1075052604'],
    x="Time",
    y="value", 
    color="groupings",
    width=1600,
    height=700,
    title="Grupos generados por señal : hsa12_group_hsarefgaubs_C1075052604")

fig.show()
