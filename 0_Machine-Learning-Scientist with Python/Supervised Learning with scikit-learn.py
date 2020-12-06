# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 11:38:29 2020

@author: crf005r
"""
#¿Que es machine learning?

#Es la ciencia y el arte de darles a las computadoras capacidad de aprender a tomar decisiones a partir de datos sin ser programado explícitamente.

#Ejemplos:

#Tenemos etiquetas -> Aprendizaje Supervisado

    #Nuestra computadora puede aprender a predecir si un correo electrónico es spam o no dado su contenido y remitente.

#No tenemos etiquetas -> Aprendizaje No Supervisado -> La escencia de este metodo es descubrir patrones y estructuras ocultas a partir de datos sin etiquetar.

    #Clasificación de entradas de Wikipedia en función de las palabras que contienen. Luego cada artículo nuevo puede ser asignado a uno de los grupos existentes.
    
    #Clasificación de clientes 
    
#Aprendizaje Por Refuerzo -> Maquinas o Agentes interactúan con un entorno, los agentes de refuerzo pueden descubrir automáticamente cómo optimizar su comportamiento dado un sistema de recompensas y castigos.

    #Aplicaciones en Economía, Genética, Videojuegos.
    
    #2016 se ocupo para entrenar a Google DeepMind

    #AlphaGo

#########################
#Aprendizaje Supervisado#
#########################

#Tenemos varios puntos de datos o muestras descrito usando variables o características predictoras y una variable objetivo.

#Ejemplo la tabla iris: Variables predictoras (Sepal, Petal) y Variable Objetivo (Species)

#El objetivo del aprendizaje supervisado es construir un modelo que pueda predecir la variable objetivo.

    #Clasificación: Variable objetivo consiste en definir una categoría.
    
        #Predecir la Especie de una flor apartir de sus medidas de Sepal Y Petal.
    
    #Regresion: Variable objetivo es continua.

        #Precio de una casa.
        
 #Nota: Features = predictor variables = independent variables 
 
       #Target variable = dependent variable = response variable

#El objetivo del aprendizaje supervisado es con frecuencia automatizar una tarea manual costosa o que lleva mucho tiempo, como:

    #Un diagnóstico médico
    
    #Predicciones sobre el futuro
    
    #Si un cliente hará un clic en un anuncio
    
    
#Para el aprendizaje supervisado, necesitamos datos etiquetados y hay muchas formas de obtenerlos.

    #Datos historico ya etiquetados
    
    #Experimentos para obtener datos etiquetados, como pruebas A/B 
    
    #Datos etiquetados de colaboración colectiva
    
#En cualquier caso, el objetivo es aprender de los datos para los que se obtiene la salida correcta y podamos hacer predicciones sobre nuevos datos para los que no conocemos el resultado.

#Existen muchas maneras de hacer Aprendizaje Supervisado con Python.

#Utilizaremos scikit-learn, una de las bibliotecas más populaes y fáciles de usar para Python.

    #Se integra muy bien con SciPy Y Numpy
    
    #Existen otras bibliotecas como Tensorflow y Keras pero lo recomendable es familiarizarze con Scikit-Learn primero.
    

#Classification

#Regression

#Fine-tuning your model

#Preprocessing and pipelines