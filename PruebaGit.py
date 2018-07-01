import os
import glob
import pandas as pd
import numpy as np

print(os.getcwd()) #Vemos la ruta en que estamos con os.chdir('Nuevo_Directorio')

pattern = '*.csv'
archivo_csv = glob.glob(pattern) #Archivos csv que tenemos en la ruta
print(archivo_csv)

columnas = ['items.id', 'items.label', 'items.authors', 'items.journal','items.country', 'items.year', 'items.date', 'items.month','items.url']

df1 = pd.read_csv('Publicaciones.csv', encoding='latin-1',header = 0,names = columnas, na_values={'items.year':['1966']})

df1.info()



