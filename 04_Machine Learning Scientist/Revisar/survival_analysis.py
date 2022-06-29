# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 21:35:12 2021

@author: Maste
"""

import pandas as pd
import numpy as np

#data = pd.read_csv("C:/Users/crf005r/Walmart Inc/Rotación People - Datos/datos_empleados/union data empleados/data_emp.csv")
data = pd.read_csv("C:/Users/Maste/Downloads/data_emp.csv")
data.info()
data = data.fillna(0)
data.isnull().all()
#Preparando datos

data = data[data["months_old"] > 0] 

data["rot"] = data["event_assoc_status"].apply(lambda x: 0 if (x == 'Active') else 1)
data = data.iloc[:,1:]
#Data de entrenamiento para el modelo

data_emp = data[ data["first_job_title_r"].isin(['cajero', 'perecederos']) &
                 data["event_reason_r"].isin(['renuncia', 'no aplica']) ]

data_emp = data_emp[data_emp["months_old"] < data_emp["months_old"].quantile(.95)]

data_emp_rot = data_emp[data_emp["event_reason_r"] == 'renuncia']

# Prueba con activos

data_activos =data[ (data["first_job_title_r"].isin(["cajero","perecederos"])) & 
                    (data["rot"] == 0) ]

#Filtros cajeros y perecederos

data_cajeros = data[data["first_job_title_r"].isin(['cajero'])]
data_perecederos = data[data["first_job_title_r"].isin(['perecederos'])]


data_cajeros.head()
data_cajeros.columns

tmp = data_cajeros[data_cajeros["rot"] == 1]

# Datos censurado, son los casos que no han occurrido
def check_observed(row):
    if pd.isna(row['hire_date']):
        flag = 0
    elif pd.isna(row['event_effective_end_date']):
        flag = 0
    else:
        flag = 1
    return flag
  
# Create a censorship flag column
data_cajeros['observed'] = data_cajeros.apply(check_observed, axis=1)

# Print average of observed
print(np.average(data_cajeros['observed']))

# Print first row
print(data_cajeros.head(1))

# Count censored data
count = len(data_cajeros[data_cajeros['rot'] == 1])

# Print the count to console
print(count)
data_cajeros.groupby(["rot","observed"]).count()

import lifelines
import matplotlib.pyplot as plt

data_cajeros.columns
data_cajeros.groupby(["range_age"]).count()

###--menos de 1 año
a_0 = data_cajeros[data_cajeros["range_age"].str.contains("menos de 1 año")]
a_0.groupby(["range_age"]).count()

kmf = lifelines.KaplanMeierFitter()
kmf.fit(round(a_0["months_old"]), a_0["rot"])

kmf.plot_survival_function()
plt.show()

###--1 a 3 años
a = data_cajeros[data_cajeros["range_age"].str.contains("1 a 3 años")]
a.groupby(["range_age"]).count()

kmf = lifelines.KaplanMeierFitter()
kmf.fit(round(a["months_old"]), a["rot"])

kmf.plot_survival_function()
plt.show()

####-- 3 a 10 años
b = data_cajeros[data_cajeros["range_age"].str.contains("3 a 10 años")]
b.groupby(["range_age"]).count()

kmf = lifelines.KaplanMeierFitter()
kmf.fit(round(b["months_old"]), b["rot"])

kmf.plot_survival_function()
plt.show()

####-- 3 a 10 años
c = data_cajeros[data_cajeros["range_age"].str.contains("mas de 10 años")]
c.groupby(["range_age"]).count()

kmf = lifelines.KaplanMeierFitter()
kmf.fit(round(c["months_old"]), c["rot"])

kmf.plot_survival_function()
plt.show()
