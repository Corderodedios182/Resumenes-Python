#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 21:50:38 2020

@author: carlos
"""


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('https://assets.datacamp.com/production/repositories/628/datasets/35a8c54b79d559145bbeb5582de7a6169c703136/house-votes-84.csv')

df.columns = ['party', 'infants', 'water', 'budget', 'physician', 'salvador','religious', 'satellite', 'aid', 
              'missile', 'immigration', 'synfuels','education', 'superfund', 'crime', 'duty_free_exports', 'eaa_rsa']


# votos hechos por los Congresistas de la Cámara de Representantes de EE. UU. 

df.head()
df.party.value_counts()
df.keys()

#remplazar yes y no por 0 y 1 

df.groupby(['education','party']).count()

plt.figure()
sns.countplot(x='missile', hue='party', data=df, palette='RdBu')
plt.xticks([0,1], ['No', 'Yes'])
plt.show()


# objetivo predecir su afiliación partidaria ('demócrata' o 'republicano') en función de cómo votaron sobre ciertos temas clave.





# vale la pena señalar que se ha preprocesado este conjunto de datos para tratar con los valores faltantes.







