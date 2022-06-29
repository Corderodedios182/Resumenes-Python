# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 11:26:00 2021

@author: crf005r
"""
import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

#data = pd.read_csv("C:/Users/crf005r/Walmart Inc/Rotación People - Datos/datos_empleados/union data empleados/data_emp.csv")
data = pd.read_csv("C:/Users/crf005r/Walmart Inc/Rotación People - Datos/datos_empleados/union data empleados/data_emp_model.csv")
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

#########
#Model 1#
#########

# Matrices para las características y el objetivo: X, y
X, y = data.iloc[:,:-1], data.iloc[:,-1]

# Crea los conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test= train_test_split(X, y, test_size=.20, random_state=123)

# instancia del XGBClassifier: xg_cl
xg_cl = xgb.XGBClassifier(objective='binary:logistic', n_estimators=5, seed=123)

# Montar la clasificadora en el set de entrenamiento.
xg_cl.fit(X_train, y_train)

# Predecir las etiquetas del conjunto de prueba: preds
preds = xg_cl.predict(X_test)

# Presicion
accuracy = float(np.sum(preds==y_test))/y_test.shape[0]
print("accuracy: %f" % (accuracy))

X_test["y_test"] = y_test
X_test["preds"] = preds

#########
#Model 2#
#########

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler

#Standarizacion de variables
scaler = StandardScaler()
X, y = data.iloc[:,:-1], data.iloc[:,-1]
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

#Creacion de train y test
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=.20, random_state=123)

#Instanciadno clasificador dt_clf_4
dt_clf_4 = DecisionTreeClassifier(max_depth = 5)

# Fit con datos de entrenamiento
dt_clf_4.fit(X_train, y_train)

# Prediccion con datos de X_test: y_pred_4
y_pred_4 = dt_clf_4.predict(X_test)

X_test["y_test"] = y_test
X_test["y_pred_4"] = y_pred_4

# Presicion
accuracy = float(np.sum(y_pred_4==y_test))/y_test.shape[0]
print("accuracy:", accuracy)










