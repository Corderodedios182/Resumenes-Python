# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 12:27:19 2020

@author: crf005r
"""

from scipy.cluster.vq import kmeans, vq
from matplotlib import pyplot as plt
import seaborn as sns, pandas as pd
from scipy.cluster.vq import whiten
import plotly.express as px
from numpy import random

import plotly.io as pio
pio.renderers.default = "browser"

random.seed(12)

data = pd.read_csv('C:/Users/crf005r/Documents/2_Adsocial/Marketing-master/Ofiices Depot/bases/Analytics/transformacion_analytics.csv')

data.columns

data["tasa_conversion_electronico"] = data["tasa_conversion_electronico"] * 100
summary = data.describe()

data = data[(data.tasa_conversion_electronico > .75) & (data.tasa_conversion_electronico < 1.75) ]
data.columns

###################
#Metodo jerarquico#
###################

#Probar agrupaciones de este metodo

########
#normal#
########

#Algoritmo
cluster_centers, _ = kmeans(data.iloc[:, [1,4]], 6)
data['cluster_labels'], _ = vq(data.iloc[:, [1,4]], cluster_centers)

#¿Cuantos cluster?
#Metodo del codo y brazo
distortions = []
num_clusters = range(1, 7)

# Create a list of distortions from the kmeans function
for i in num_clusters:
    cluster_centers, distortion = kmeans(data.iloc[:, [1,4]], i)
    distortions.append(distortion)

# Create a data frame with two lists - num_clusters, distortions
elbow_plot = pd.DataFrame({'num_clusters': num_clusters, 'distortions': distortions})

# Creat a line plot of num_clusters and distortions
sns.lineplot(x="num_clusters", y="distortions", data = elbow_plot)
plt.xticks(num_clusters)
plt.show()

fig = px.scatter(data, x="Suma de ingresos",
                       y="tasa_conversion_electronico",
                       color="cluster_labels",
                       hover_data=["audiencia"],
                       title = "K-means, sin normalizar los datos")
fig.show()

##############################
#Datos estandarizados (Mejor)#
##############################

data["scaled_ingresos"] , data["scaled_tasa"] = whiten(data["Suma de ingresos"]), whiten(data["tasa_conversion_electronico"])

#Algoritmo
cluster_centers, _ = kmeans(data.iloc[:, [6,7]], 8)
data['cluster_labels_scaled'], _ = vq(data.iloc[:, [6,7]], cluster_centers)

#Resultados
fig = px.scatter(data, x="scaled_ingresos",
                       y="scaled_tasa",
                       color="cluster_labels_scaled",
                       hover_data=["audiencia"],
                       title = "K-means, datos normalizados")
fig.show()
fig.write_html("grafica_1.html")

#Audiencia
audiencia = data.groupby(["cluster_labels_scaled"], as_index = False).sum()
audiencia["tasa_conversion"] = (audiencia["Suma de transacciones"] / audiencia["Suma de sesiones"])*100
audiencia = audiencia.loc[:,["Suma de ingresos","tasa_conversion"]]

import pandas as pd

matrix = pd.read_csv("C:/Users/crf005r/Documents/2_Adsocial/Marketing-master/Ofiices Depot/bases/Analytics/analytics_prueba.csv")

matrix = matrix.values.tolist()

# Names of the features.
names = ["C_0", "C_1", "C_2",
         "C_3", "C_4", "C_5",
         "C_6",  "C_7"]

from chord import Chord

# Pass the list to the colors parameter.
Chord(matrix, names).show()

Chord(matrix, names).to_html()
Chord(matrix, names, colors = f"d3.schemeGnBu[{len(names)}]").to_html()






