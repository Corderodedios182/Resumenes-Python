#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 14:05:14 2019

@author: carlos
"""

import pandas as pd

police = pd.read_csv('https://assets.datacamp.com/production/repositories/1497/datasets/62bd9feef451860db02d26553613a299721882e8/police.csv')

weather = pd.read_csv('https://assets.datacamp.com/production/repositories/1497/datasets/02f3fb2d4416d3f6626e1117688e0386784e8e55/weather.csv')

police.shape
police.info()
#Eliminamos county_name ya que solo tiene columnas nulas
police.isnull().sum()
#De igual forma state solo tiene valores de RI (Rhode Island)
police.state.value_counts()

police.drop(['county_name', 'state'], axis='columns', inplace=True)
police.shape

#Tenemos 5205 filas faltantes eliminaremos las filas faltantes de la columna driver_gender
police.dropna(subset=['driver_gender'], inplace=True)
police.isnull().sum()

police.dtypes
#Tipos de datos adecuados 
police.is_arrested.value_counts()

police.is_arrested = police.is_arrested.astype('bool')
police.is_arrested.dtypes

#Trabajando con fechas
police.loc[:,['stop_date','stop_time']].dtypes

police.stop_date.value_counts().head()
police.stop_time.value_counts().head()

#Combinaremos las columnas stop_date y stop_time para luego convertir en formato datetime
combined = police.stop_date.str.cat(police.stop_time, sep=' ')

police['stop_datetime'] = pd.to_datetime(combined)
police.dtypes

police.set_index('stop_datetime', inplace = True)
police.head()

#Examinación jerarquica de los datos
#Antes de comenzar con preguntas puntuales de los datos, es una buena práctica comenzar con los resumens más generales

#Examinando las infracciones de tránsito
#Conteo
police.violation.value_counts()
#Porcentaje
police.violation.value_counts(normalize = True)

#Comparaciones de violaciones por Generó 

male = police[police.driver_gender == 'M']
female = police[police.driver_gender == 'F']

male.violation.value_counts(normalize = True)
female.violation.value_counts(normalize = True)
#Alrededor de dos tercios de las paradas de tráfico femenino son para acelerar,
# mientras que las paradas de los hombres están más equilibradas entre las seis categorías.
#Sin embargo, esto no significa que las mujeres aceleren más a menudo que los hombres,
#ya que no tomamos en cuenta la cantidad de paradas o conductores.

#¿El género afecta a quién recibe una multa por exceso de velocidad?

female_and_speeding = police[(police.driver_gender == 'F') & (police.violation == 'Speeding')]

male_and_speeding = police[(police.driver_gender == 'M') & (police.violation == 'Speeding')]

print(female_and_speeding.stop_outcome.value_counts(normalize=True))

print(male_and_speeding.stop_outcome.value_counts(normalize=True))

#¡Interesante! Los números son similares para hombres y mujeres:
#alrededor del 95% de las paradas por exceso de velocidad resultan en una multa.
#Por lo tanto, los datos no muestran que el género tiene un impacto en quién recibe una multa por exceso de velocidad.

#¿El género afecta a quién se le raliza una busqueda?

#Durante una parada de tráfico, el oficial de policía a veces realiza una búsqueda del vehículo.
#En este ejercicio, calculará el porcentaje de todas las paradas que resultan en una búsqueda de vehículo,
#también conocida como la tasa de búsqueda.

police.search_conducted.value_counts(normalize = True)
police.search_conducted.mean()

#¡Excelente! Parece que la tasa de búsqueda es de aproximadamente 3.8%.
#A continuación, examinará si la tasa de búsqueda varía según el género del conductor.

#comparará las tasas a las que se busca a los conductores femeninos y masculinos durante una parada de tráfico. Recuerde que la tasa de búsqueda de vehículos en todas las paradas es de aproximadamente 3.8%.
print(police.groupby('driver_gender').search_conducted.mean())

#¡Guauu! Los conductores masculinos son buscados más del doble de veces que los conductores femeninos.
#¿Por qué podría ser esto?
print(police.groupby(['driver_gender', 'violation']).search_conducted.mean())
print(police.groupby(['violation', 'driver_gender']).search_conducted.mean())
#¡Buen trabajo! Para todos los tipos de violaciones, la tasa de búsqueda es más alta para hombres que para mujeres, lo que refuta nuestra hipótesis.

#Durante la búsqueda de un vehículo, el oficial de policía puede golpear al conductor para verificar si
#tiene un arma.
# Esto se conoce como un "registro protector".

#En este ejercicio, primero verificará cuántas veces "Protective Frisk" fue el único tipo de búsqueda.
#Luego, usará un método de cadena para localizar todas las instancias en las que se registró el controlador.

print(police.search_type.value_counts())
police['frisk'] = police.search_type.str.contains('Protective Frisk', na=False)
print(police.frisk.dtype)
print(police.frisk.sum())

#¡Buen trabajo! Parece que hubo 303 conductores que fueron cacheados.
#A continuación, examinará si el género afecta a quién se registra

#Comparación de tasas de registro por género
#¿Se registran los hombres con más frecuencia que las mujeres, tal vez porque los policías los consideran de mayor riesgo?

# Create a DataFrame of stops in which a search was conducted
searched = police[police.search_conducted == True]
print(searched.frisk.mean())

# Calculate the frisk rate for each gender
print(searched.groupby('driver_gender').frisk.mean())

#¡Interesante! La tasa de registro es más alta para los hombres que para las mujeres, aunque no podemos concluir que esta diferencia sea causada por el género del conductor.

#Analisis exploratorio visual

#¿La hora del día afecta la tasa de arresto?

print(police.is_arrested.mean())

print(police.groupby(police.index.hour).is_arrested.mean())

# Save the hourly arrest rate
hourly_arrest_rate = police.groupby(police.index.hour).is_arrested.mean()

import matplotlib.pyplot as plt

hourly_arrest_rate.plot()

# Add the xlabel, ylabel, and title
plt.xlabel('Horas')
plt.ylabel('Tasa de arresto')
plt.title('Tasa de Arresto por hora del día')

#¡Guauu! La tasa de arrestos tiene un pico significativo durante la noche, y luego cae en las primeras horas de la mañana.

#¿Están aumentando las paradas relacionadas con las drogas?
print(police.drugs_related_stop.resample('A').mean())

annual_drug_rate = police.drugs_related_stop.resample('A').mean()
annual_drug_rate.plot()

#Comparación de drogas y tasas de búsqueda de drogas

# Calculate and save the annual search rate
annual_search_rate = police.search_conducted.resample('A').mean()

# Concatenate 'annual_drug_rate' and 'annual_search_rate'
annual = pd.concat([annual_drug_rate, annual_search_rate], axis='columns')

# Create subplots from 'annual'
annual.plot(subplots=True)

#¡Guauu! La tasa de paradas relacionadas con las drogas aumentó a pesar de que la tasa de búsqueda disminuyó, refutando nuestra hipótesis.

#¿Qué infracciones se detectan en cada distrito?

# Create a frequency table of districts and violations
print(pd.crosstab(police.district, police.violation))

# Save the frequency table as 'all_zones'
all_zones = pd.crosstab(police.district, police.violation)

# Select rows 'Zone K1' through 'Zone K3'
print(all_zones.loc['Zone K1':'Zone K3'])

# Save the smaller table as 'k_zones'
k_zones = all_zones.loc['Zone K1':'Zone K3']

# Create a bar plot of 'k_zones'
k_zones.plot(kind='bar')

# Create a stacked bar plot of 'k_zones'
k_zones.plot(kind='bar', stacked=True)

#¡Interesante! La gran mayoría de las paradas de tráfico en la Zona K1 son por exceso de velocidad, y las Zonas K2 y K3 son notablemente similares entre sí en términos de violaciones.

#¿Cuánto tiempo podría ser detenido por una violación?
# Print the unique values in 'stop_duration'
print(police.stop_duration.unique())

# Create a dictionary that maps strings to integers
mapping = {'0-15 Min':8, '16-30 Min':23, '30+ Min':45}

# Convert the 'stop_duration' strings to integers using the 'mapping'
police['stop_minutes'] = police.stop_duration.map(mapping)

# Print the unique values in 'stop_minutes'
print(police.stop_minutes.unique())

#¡Excelente! A continuación, analizará la duración de la detención para cada tipo de infracción.

#visualizará el tiempo promedio que los conductores están detenidos por cada tipo de violación. En lugar de usar la violationcolumna en este ejercicio, la usará violation_rawya que contiene descripciones más detalladas de las violaciones.

# Calculate the mean 'stop_minutes' for each value in 'violation_raw'
print(police.groupby('violation_raw').stop_minutes.mean())

# Save the resulting Series as 'stop_length'
stop_length = police.groupby('violation_raw').stop_minutes.mean()

# Sort 'stop_length' by its values and create a horizontal bar plot
stop_length.sort_values().plot(kind='barh')

#En este ejercicio, examinará las columnas de temperatura del conjunto de datos meteorológicos para evaluar
#si los datos parecen confiables.
#Primero imprimirá las estadísticas de resumen, y luego visualizará los datos usando un diagrama de caja.

#¡Al decidir si los valores parecen razonables, tenga en cuenta que la temperatura se mide en grados Fahrenheit, no en grados Celsius!
weather.head()

print(weather[['TMIN', 'TAVG', 'TMAX']].describe())

# Create a box plot of the temperature columns
weather[['TMIN', 'TAVG', 'TMAX']].plot(kind='box')

# Create a 'TDIFF' column that represents temperature difference
weather['TDIFF'] = weather.TMAX - weather.TMIN

# Describe the 'TDIFF' column
print(weather.TDIFF.describe())

# Create a histogram with 20 bins to visualize 'TDIFF'
weather.TDIFF.plot(kind='hist', bins=20)

#El weatherDataFrame contiene 20 columnas que comienzan con 'WT', cada una de las cuales representa una mala condición climática. Por ejemplo:

#WT05 indica "granizo"
#WT11 indica "vientos fuertes o dañinos"
#WT17 indica "lluvia helada"
#Para cada fila de la base de datos, cada WTcolumna contiene o bien un 1(es decir, la condición estaba presente ese día) o NaN(es decir, la condición no estaba presente).

# Copy 'WT01' through 'WT22' to a new DataFrame
WT = weather.loc[:, 'WT01':'WT22']

# Calculate the sum of each row in 'WT'
weather['bad_conditions'] = WT.sum(axis='columns')

# Replace missing values in 'bad_conditions' with '0'
weather['bad_conditions'] = weather.bad_conditions.fillna(0).astype('int')

# Create a histogram to visualize 'bad_conditions'
weather.bad_conditions.plot(kind='hist')

#¡Excelente trabajo! Parece que muchos días no tuvieron condiciones climáticas adversas, y solo una pequeña parte de los días tuvo más de cuatro condiciones climáticas adversas.

#Calificación de las condiciones climáticas

# Count the unique values in 'bad_conditions' and sort the index
print(weather.bad_conditions.value_counts().sort_index())

# Create a dictionary that maps integers to strings
mapping = {0:'good', 1:'bad', 2:'bad', 3:'bad', 4:'bad', 5:'worse', 6:'worse', 7:'worse', 8:'worse', 9:'worse'}

# Convert the 'bad_conditions' integers to strings using the 'mapping'
weather['rating'] = weather.bad_conditions.map(mapping)

# Count the unique values in 'rating'
print(weather.rating.value_counts())

#¡Buen trabajo! Este sistema de clasificación debería facilitar la comprensión de los datos de las condiciones climáticas.

#Cambiar el tipo de datos a categoría
#Dado que la ratingcolumna solo tiene algunos valores posibles, cambiará su tipo de datos a categoría para almacenar los datos de manera más eficiente. También especificará un orden lógico para las categorías, que será útil para futuros ejercicios.

# Create a list of weather ratings in logical order
cats = ['good', 'bad', 'worse']

# Change the data type of 'rating' to category
weather['rating'] = weather.rating.astype('category', ordered=True, categories=cats)

# Examine the head of 'rating'
print(weather.rating.head())

#Preparando los datos para unirlos

# Reset the index of 'ri'
police.reset_index(inplace=True)

# Examine the head of 'ri'
print(police.head())

# Create a DataFrame from the 'DATE' and 'rating' columns
weather_rating = weather[['DATE', 'rating']]

# Examine the head of 'weather_rating'
print(weather_rating.head())

# Examine the shape of 'ri'
print(police.shape)

# Merge 'ri' and 'weather_rating' using a left join
police_weather = pd.merge(left=police, right=weather_rating, left_on='stop_date', right_on='DATE', how='left')

# Examine the shape of 'ri_weather'
print(police_weather.shape)

# Set 'stop_datetime' as the index of 'ri_weather'
police_weather.set_index('stop_datetime', inplace=True)

#¡Fantástico! En la siguiente sección, usará ri_weatherpara analizar la relación entre las condiciones climáticas y el comportamiento policial.

#¿El clima afecta la tasa de arresto?
print(police_weather.is_arrested.mean())

print(police_weather.groupby('rating').is_arrested.mean())

print(police_weather.groupby(['violation', 'rating']).is_arrested.mean())

#¡Guauu! La tasa de arrestos aumenta a medida que el clima empeora, y esa tendencia persiste en muchos de los tipos de violación. Esto no prueba un vínculo causal, ¡pero es un resultado bastante interesante!

# Save the output of the groupby operation from the last exercise
arrest_rate = police_weather.groupby(['violation', 'rating']).is_arrested.mean()

# Print the 'arrest_rate' Series
print(arrest_rate)

# Print the arrest rate for moving violations in bad weather
print(arrest_rate.loc['Moving violation', 'bad'])

# Print the arrest rates for speeding violations in all three weather conditions
print(arrest_rate.loc['Speeding'])

# Unstack the 'arrest_rate' Series into a DataFrame
print(arrest_rate.unstack())

# Create the same DataFrame using a pivot table
print(police_weather.pivot_table(index='violation', columns='rating', values='is_arrested'))









