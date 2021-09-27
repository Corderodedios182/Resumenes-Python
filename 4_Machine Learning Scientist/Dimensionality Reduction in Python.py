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

salary_df = pd.read_csv("C:/Users/Maste/Documents/1_Github/Resumenes-Python/4_Machine Learning Scientist/datos/salary_programmers.csv")
salary_df = salary_df.fillna(0)

######################################
#Reduccion de los datos por relevntes#
######################################

#Conociendo los datos de forma rápida.
salary_df.info()
salary_df.describe(exclude=('number'))
salary_df.describe()

#Division de columnas numericas y no numericas
drop_cols = ["id","timestamp"]
salary_df = salary_df.drop(drop_cols, axis = 1)
non_number_cols = ['country', 'employment_status', 'job_title', 'is_manager', 'education', 'is_education_computer_related', 'certifications']
number_cols = ['job_years', 'hours_per_week', 'telecommute_days_per_week', 'salary']

#Reordenado y seleccionando columnas importantes para una mejor visualizacion
salary_df = salary_df[non_number_cols + number_cols]
print(salary_df.head())

#Resumen de los paises
y = np.array(salary_df["country"].value_counts(normalize = True))
mylabels = salary_df["country"].value_counts(normalize = True).index
plt.pie(y, labels = mylabels)

#Graficando las variables relevantes
sns.pairplot(salary_df, hue='country', diag_kind='hist')

#Libreria para un resumen rapido de los datos en Jupyter.
import pandas_profiling as pp
from pandas_profiling import ProfileReport

salary_df.profile_report(style={'full_width':True})
profile = ProfileReport(salary_df, title="Pandas Profiling Report")
ProfileReport(salary_df, title="Pandas Profiling Report", explorative=True)
profile.to_widgets()

################################################
#visualización t-SNE de datos de alta dimensión#
################################################

#¿Cuál es un buen caso de uso para usar t-SNE?
#Cuando desee explorar visualmente los patrones en un conjunto de datos de alta dimensión.

#Trabaja con datos no numericos
salary_numeric = salary_df.drop(non_number_cols, axis = 1)

from sklearn.manifold import TSNE
#La incrustación de vecinos estocásticos distribuidos en t (t-SNE) es un método estadístico para visualizar datos de alta dimensión
#dando a cada punto de datos una ubicación en un mapa bidimensional o tridimensional.
#Se basa en la incrustación de vecinos estocástica 

#Es una reducción de dimensionalidad no lineal.
#Técnica muy adecuada para incrustar datos de alta dimensión para visualización en un espacio de baja dimensión de dos o tres dimensiones.
#Específicamente, modela cada objeto de alta dimensión por un punto bidimensional o tridimensional de tal manera que 
#objetos similares son modelados por puntos cercanos y objetos diferentes son modelados por puntos distantes con alta probabilidad.

m = TSNE(learning_rate=50)

tsne_features = m.fit_transform(salary_numeric)

salary_df["x"] = tsne_features[:,0]

salary_df["y"] = tsne_features[:,1]

import seaborn as sns

#Si bien los gráficos de t-SNE a menudo parecen mostrar grupos ,
#los grupos visuales pueden verse fuertemente influenciados por la parametrización elegida y, por lo tanto,
#es necesaria una buena comprensión de los parámetros de t-SNE.

#Se puede demostrar que tales "grupos" incluso aparecen en datos no agrupados,
#y, por lo tanto, pueden ser resultados falsos.

#Por tanto, la exploración interactiva puede ser necesaria para elegir parámetros y validar los resultados
sns.scatterplot(x = "x", y = "y", hue = "country", data= salary_df)
sns.scatterplot(x = "x", y = "y", hue = "employment_status", data= salary_df)
sns.scatterplot(x = "x", y = "y", hue = "job_title", data= salary_df)
sns.scatterplot(x = "x", y = "y", hue = "is_manager", data= salary_df)
sns.scatterplot(x = "x", y = "y", hue = "education", data= salary_df)
sns.scatterplot(x = "x", y = "y", hue = "is_education_computer_related", data= salary_df)
sns.scatterplot(x = "x", y = "y", hue = "certifications", data= salary_df)

#Se ha demostrado que t-SNE a menudo es capaz de recuperar agrupaciones bien separadas y, 
#con opciones especiales de parámetros, se aproxima a una forma simple de agrupación espectral 

##############################
#Selección de Características#
##############################

#Aprenderá sobre la maldición de la dimensionalidad y cómo la reducción de la dimensionalidad puede ayudarlo a superarla.
#Se le presentará una serie de técnicas para detectar y eliminar características que aportan poco valor agregado al conjunto de datos.
#Ya sea porque tienen poca varianza, demasiados valores perdidos o porque están fuertemente correlacionados con otras características.

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

lb_make = LabelEncoder()
pokemon_df['Type 1'] = lb_make.fit_transform(pokemon_df['Type 1'])
pokemon_df['Type 2'] = lb_make.fit_transform(pokemon_df['Type 2'])

X = pokemon_df.drop(["Name","#","Total","Generation"], axis = 1)
y = pokemon_df["Generation"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= .30)

svc = SVC()
svc.fit(X_train, y_train)

print(accuracy_score(y_test, svc.predict(X_test))) #Erro
print(accuracy_score(y_train, svc.predict(X_train))) #Error de entrenamiento










