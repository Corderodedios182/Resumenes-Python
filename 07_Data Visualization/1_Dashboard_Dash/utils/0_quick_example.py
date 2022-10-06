import os
os.chdir("C:\\Users\\cflorelu\\Documents\\Github\\Resumenes-Python\\07_Data Visualization\\1_Dashboard_Dash")

import pandas as pd
import dask.dataframe as dd

# Plotly graph objects to render graph plots
import plotly.graph_objects as go
import plotly.express as px

#import plotly.io as pio
#pio.renderers.default='browser'
ddf_may = dd.read_csv("data/ddf_dash/df_ideal.csv").compute()

ddf_signal = dd.read_csv("data/ddf_signal/*.csv").compute()
ddf_signal['Time'] = pd.to_datetime(ddf_signal['Time'])

#ddf_signal = ddf_signal.loc[:,["Time",
#                               "groupings",
#                               "s4_drv_net_a_ea_seg12_linear_speed_C1074856027", "hsa12_group_hsarefgauts_C1075052603","hsa12_group_hsarefgaubs_C1075052604","hsa12_group_hsasegid_C1075052607"]]

ddf_signal = pd.melt(ddf_signal,
                       id_vars = ["Time",'groupings'],
                       value_vars = ddf_signal.columns[2:])

def quick_example(signal):
    fig = px.scatter(
        ddf_signal[ddf_signal["variable"] == signal],
        x="Time",
        y="value", 
        color="groupings",
        width=1600,
        height=700,
        title=r"Grupos generados por señal : {}".format(signal))

    fig.show()

    return ddf_may[ddf_may["signal"] == signal].loc[:,["day","key_group","Count_may22","outlierDown_may22","outlierUp_may22","Cantidad_CU_may22",'pct_val_no_zeros', 'pct_val_equal_zero',
                                                        'pct_val_null', 'sum_validation_completeness', 'within_range','out_lower_range', 'out_upper_range',
                                                        'indicator']]
signal = "s4_drv_net_a_ea_seg012_trq_cmd_C1611726945"
#signal = "hsa12_group_hsasegid_C1075052607"

quick_example(signal)