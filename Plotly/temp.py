# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import plotly
# plotly.__version__

import plotly.dashboard_objs as dashboard
import plotly.plotly as py
import plotly.graph_objs as go

from datetime import datetime
import IPython.display
from IPython.display import Image
import numpy as np
import pandas as pd
import pandas_datareader.data as web

import urllib3
urllib3.disable_warnings()

#Style & Colorscheme

colors = []
colorscales = 'Blues'

#Choose Plots
"C:\Users\carlos.flores\OneDrive - Interpublic\Desktop\Carlos\Modelos\"
df = web.DataReader('TUD', 'oecd', end = datetime(2018,1,1))

Mexico = df[['Mexico']]
Mexico.head()





