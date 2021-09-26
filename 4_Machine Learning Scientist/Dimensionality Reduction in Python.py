# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 16:31:13 2021

@author: Maste
"""

#Se le presentará el concepto de reducción de dimensionalidad y aprenderá cuándo y por qué esto es importante.
#Aprenderá la diferencia entre la selección de características y la extracción de características y aplicará ambas técnicas para la exploración de datos.
#El capítulo termina con una lección sobre t-SNE, una poderosa técnica de extracción de características que le permitirá visualizar un conjunto de datos
# de alta dimensión

import pandas as pd
import seaborn as sns
import matplotlib as plt
import numpy as np

pokemon_df = pd.read_csv("C:/Users/Maste/Documents/1_Github/Resumenes-Python/4_Machine Learning Scientist/datos/pokemon.csv")

pokemon_df.info()

pokemon_df.describe(exclude=('number'))
pokemon_df.describe()

# Remove the feature without variance from this list
number_cols = ['HP', 'Attack', 'Defense']

# Leave this list as is for now
non_number_cols = ['Name', 'Type 1', 'Legendary']

# Sub-select by combining the lists with chosen features
df_selected = pokemon_df[number_cols + non_number_cols]

# Prints the first 5 lines of the new dataframe
print(df_selected.head())
df_selected["Type 1"].value_counts()
df_selected["Type 1"].value_counts(normalize = True)*100

y = np.array(df_selected["Type 1"].value_counts(normalize = True))
mylabels = df_selected["Type 1"].value_counts(normalize = True).index
plt.pie(y, labels = mylabels)

# Create a pairplot and color the points using the 'Gender' feature
sns.pairplot(df_selected, hue='Legendary', diag_kind='hist')

import pandas_profiling as pp
from pandas_profiling import ProfileReport

pokemon_df.profile_report(style={'full_width':True})
profile = ProfileReport(df_selected, title="Pandas Profiling Report")




