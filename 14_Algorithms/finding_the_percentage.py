# -*- coding: utf-8 -*-
"""
Spyder Editor

Calcular el promedio de una llave en especifico de un diccionario

"""

if __name__ == '__main__':
    n = int(input())
    #diccionario donde almacenamos key = nombre , value = lista de scores
    student_marks = {}
    # lee y guarda nombres, lista de scores
    for _ in range(n):
        name, *line = input().split()
        scores = list(map(float, line))
        student_marks[name] = scores
    #Especificamos el query_name
    query_name = input()

#Solucion: Extraer el query_name y calcula el promedio
    
print('{0:.2f}'.format(sum(student_marks[query_name])/len(student_marks[query_name])))

#Ejemplo de insumos para correr el scrip tal cual se copian.

#3
#Krishna 67 68 69
#Arjun 70 98 63
#Malika 52 56 60
#Malika