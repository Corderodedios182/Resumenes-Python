# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 12:27:19 2020

@author: crf005r

El siguiente scrip contiene lo necesario para realizar un Modelo de Cluster sobre un conjunto de datos

- Metodo Jerarquico.
    Dendograma
- Kmeans
    Grafica de codo
- Aplicaciones del mundo real

"""

from numpy import random
import seaborn as sns, pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.io as pio
from chord import Chord #Grafica Chord 
import matplotlib.image as img #Lectura de imagenes

pio.renderers.default = "browser"

from scipy.cluster.hierarchy import linkage, fcluster #Jerarquico
from scipy.cluster.hierarchy import dendrogram #dendograma

from scipy.cluster.vq import kmeans, vq #Kmeans
from scipy.cluster.vq import whiten #Estandarizacion

#Conociendo los datos
random.seed(12)

data = pd.read_csv('C:/Users/crf005r/Documents/2_Adsocial/Marketing-master/Ofiices Depot/bases/Analytics/transformacion_analytics.csv')
data.columns

data["tasa_conversion_electronico"] = data["tasa_conversion_electronico"] * 100
summary = data.describe()

data = data[(data.tasa_conversion_electronico > .75) & (data.tasa_conversion_electronico < 1.75) ]
data.columns

data["scaled_ingresos"] , data["scaled_tasa"] = whiten(data["Suma de ingresos"]), whiten(data["tasa_conversion_electronico"])

###################
#Metodo jerarquico#
###################

# Use the linkage() function, creating a distance matrix.
#method: how to calculate the proximity of cluster
#metric: distance metric
#optimal_ordering: order data points

#Whic method should use?
#single: based on two closet objects
#complete:based on two farthest objects
#average:based on the aritmetic mean of all objects
#centroid: based on the geometric mean of all objects
#median: based on the median of all objects
#ward: based on the sum of squares

methods = ["single","complete","average","centroid","median","ward"]

for method in methods:
    
    distance_matrix = linkage(data[['scaled_ingresos', 'scaled_tasa']], method = method, metric = 'euclidean')

    # Assign cluster labels
    #Create cluster labels with fcluster

    #distance_matrix: output of linkage() method
    #num:clusters: numbers of clusters
    #criterion: hoy to decide thresholds to form clusters

    #Hierachical clustering with ward method.
    data['cluster_labels'] = fcluster(distance_matrix, 5, criterion='maxclust')
    
    # Plot clusters
    sns.scatterplot(x="scaled_ingresos", y="scaled_tasa",
                    hue="cluster_labels",data=data)
    plt.xlabel("scaled_ingresos", size=16)
    plt.ylabel("scaled_tasa", size=16)
    plt.title("Usando metodo: " + method, size=24)
    plt.show()

#How many clusters?

#Dendograms
#Strategy till now - decide clusters on visual inspection
#Dendrograms help in showing progressions as clusters are merged
#A dendrogram is a branching diagram that demonstrates how each cluster is composed by branching out into its child nodes

#Create a dendogram is SciPy

for method in methods:
    
    Z = linkage(data[["scaled_ingresos","scaled_tasa"]],
                method = method,
                metric="euclidean")
    dn = dendrogram(Z)
    plt.title("Usando metodo: " + method, size = 24)
    plt.show()
    
#Measuring speed in hierarchical clustering

#timeit module
#Measure the speed of .linkage() method
#Use randomly generated points
#Run various iterations to extrapolate

#Warning, time execution
#Increasing runtime with data points
#Quadratic increase of runtime
#Not feasible for large datasets
%timeit linkage(data[["scaled_ingresos","scaled_tasa"]], method = method, metric="euclidean")

#De lo anterior podemos ver que un buen metodo para este conjunto de datos es ward
distance_matrix = linkage(data[['scaled_ingresos', 'scaled_tasa']], method = "ward", metric = 'euclidean')
data['cluster_labels'] = fcluster(distance_matrix, 7, criterion='maxclust')
    
# Plot clusters
sns.scatterplot(x="scaled_ingresos", y="scaled_tasa",
                hue="cluster_labels",data=data)
plt.xlabel("scaled_ingresos", size=16)
plt.ylabel("scaled_tasa", size=16)
plt.title("Usando metodo: " + "ward", size=24)
plt.show()

#Dendograma
dn = dendrogram(distance_matrix)

plt.title("Usando metodo: " + "ward", size = 24)
plt.show()
    
#Basic checks
#Clusters centers
centers = data.groupby('cluster_labels')[['scaled_ingresos','scaled_tasa']].mean()
centers.plot(kind='bar')

#Number in the clusters
data.groupby('cluster_labels')['cluster_labels'].count()

#Registros en cada cluster
for cluster in data['cluster_labels'].unique():
    print(cluster, data[data['cluster_labels'] == cluster]['audiencia'].values[:5])

#########
#K-means#
#########

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

#Uso de los resultados de un cluster
matrix = pd.read_csv("C:/Users/crf005r/Documents/2_Adsocial/Marketing-master/Ofiices Depot/bases/Analytics/analytics_prueba.csv")

matrix = matrix.values.tolist()

# Names of the features.
names = ["C_0", "C_1", "C_2",
         "C_3", "C_4", "C_5",
         "C_6",  "C_7"]


# Pass the list to the colors parameter.
Chord(matrix, names).show()

Chord(matrix, names).to_html()
Chord(matrix, names, colors = f"d3.schemeGnBu[{len(names)}]").to_html()

##########################
#Clustering in Real World#
##########################

#Podemos aplicar un analisis de cluster para clasificar los colores dominantes en una imagen.

image = img.imread("C:/Users/crf005r/Documents/3_GitHub/Resumenes-Python/0_Machine-Learning-Scientist with Python/mar-655x368.png")
image.shape

#Convert image to RGB matrix
r = []
g = []
b = []

for row in image:
    for pixel in row:
        #A pixel contains RGB values
        temp_r, temp_g, temp_b = pixel
        r.append(temp_r)
        g.append(temp_g)
        b.append(temp_b)

pixels = pd.DataFrame({'red':r,
                       'blue':b,
                       'green':g})

pixels.head()

#Datos estandarizado
pixels["scaled_red"] , pixels["scaled_blue"], pixels["scaled_green"] = whiten(pixels["red"]), whiten(pixels["blue"]), whiten(pixels["green"])

#Create an elbow plot
distortions = []
num_clusters = range(1,8)

#Create a list of distortions from the kmeans method
for i in num_clusters:
    cluster_centers, distortion = kmeans(pixels[['scaled_red','scaled_blue','scaled_green']], i)
    distortions.append(distortion)
    
#Create a data frame with two list - number of clusters and distorions
elbow_plot = pd.DataFrame({'num_clusters':num_clusters,
                           'distortions':distortions})

#Creat a line plot of num_clusters and distortions
sns.lineplot(x='num_clusters', y='distortions', data=elbow_plot)
plt.xticks(num_clusters)
plt.show()

#Colores dominantes dentro de la imagen, viendo el diagrama de codo.

cluster_centers, distortion = kmeans(pixels[['scaled_red','scaled_blue','scaled_green']], 2)

colors = []





















