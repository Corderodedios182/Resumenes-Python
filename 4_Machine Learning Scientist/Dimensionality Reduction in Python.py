# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 16:31:13 2021

Se le presentará el concepto de reducción de dimensionalidad y aprenderá cuándo y por qué esto es importante.
Aprenderá la diferencia entre la selección de características y la extracción de características y aplicará ambas técnicas para la exploración de datos.
El capítulo termina con una lección sobre t-SNE, una poderosa técnica de extracción de características que le permitirá visualizar un conjunto de datos
de alta dimensión

@author: Carlos Flores
"""
import pandas as pd
import seaborn as sns
import matplotlib as plt
import numpy as np

pokemon_df = pd.read_csv("C:/Users/Maste/Documents/1_Github/Resumenes-Python/4_Machine Learning Scientist/datos/pokemon.csv")

######################################
#Reduccion de los datos por relevntes#
######################################

#Conociendo los datos de forma rápida.
pokemon_df.info()
pokemon_df.describe(exclude=('number'))
pokemon_df.describe()

#Division de columnas numericas y no numericas
number_cols = ['HP', 'Attack', 'Defense']
non_number_cols = ['Name', 'Type 1', 'Legendary']

#Reordenado y seleccionando columnas importantes para una mejor visualizacion
df_selected = pokemon_df[number_cols + non_number_cols]
print(df_selected.head())

#Resumen de los tipos de Pokemon
y = np.array(df_selected["Type 1"].value_counts(normalize = True))
mylabels = df_selected["Type 1"].value_counts(normalize = True).index
plt.pie(y, labels = mylabels)

#Graficando las variables relevantes HP, Attack, Defense
sns.pairplot(df_selected, hue='Legendary', diag_kind='hist')

#Libreria para un resumen rapido de los datos en Jupyter.
import pandas_profiling as pp
from pandas_profiling import ProfileReport

pokemon_df.profile_report(style={'full_width':True})
profile = ProfileReport(pokemon_df, title="Pandas Profiling Report")
ProfileReport(pokemon_df, title="Pandas Profiling Report", explorative=True)
profile.to_widgets()

################################################
#visualización t-SNE de datos de alta dimensión#
################################################

#¿Cuál es un buen caso de uso para usar t-SNE?
#Cuando desee explorar visualmente los patrones en un conjunto de datos de alta dimensión.

#Trabaja con datos no numericos
no_numeric = ["#", "Name", "Type 1", "Type 2", "Legendary", "Total"]
pokemon_numeric = pokemon_df.drop(no_numeric, axis = 1)

from sklearn.manifold import TSNE
#La incrustación de vecinos estocásticos distribuidos en t (t-SNE) es un método estadístico para visualizar datos de alta dimensión
#dando a cada punto de datos una ubicación en un mapa bidimensional o tridimensional.
#Se basa en la incrustación de vecinos estocástica 

#Es una reducción de dimensionalidad no lineal.
#Técnica muy adecuada para incrustar datos de alta dimensión para visualización en un espacio de baja dimensión de dos o tres dimensiones.
#Específicamente, modela cada objeto de alta dimensión por un punto bidimensional o tridimensional de tal manera que 
#objetos similares son modelados por puntos cercanos y objetos diferentes son modelados por puntos distantes con alta probabilidad.

m = TSNE(learning_rate=50)

tsne_features = m.fit_transform(pokemon_numeric)

pokemon_df["x"] = tsne_features[:,0]

pokemon_df["y"] = tsne_features[:,1]

import seaborn as sns

#Si bien los gráficos de t-SNE a menudo parecen mostrar grupos ,
#los grupos visuales pueden verse fuertemente influenciados por la parametrización elegida y, por lo tanto,
#es necesaria una buena comprensión de los parámetros de t-SNE.

#Se puede demostrar que tales "grupos" incluso aparecen en datos no agrupados,
#y, por lo tanto, pueden ser resultados falsos.

#Por tanto, la exploración interactiva puede ser necesaria para elegir parámetros y validar los resultados
sns.scatterplot(x = "x", y = "y", hue = "Type 1", data= pokemon_df)
sns.scatterplot(x = "x", y = "y", hue = "Legendary", data= pokemon_df)

#Se ha demostrado que t-SNE a menudo es capaz de recuperar agrupaciones bien separadas y, 
#con opciones especiales de parámetros, se aproxima a una forma simple de agrupación espectral 
