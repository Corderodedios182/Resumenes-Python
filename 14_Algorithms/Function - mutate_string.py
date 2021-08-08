# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 14:10:10 2021

@author: crf005r
"""

#Queremos modificar una letra de una palabra
string = "abracadabra"
print(string[5])
string[5] = "k"

#Para esto debemos convertir el tipo de dato en lista
l = list(string)
l[5] = "k"
string = ''.join(l)

#Otra forma sería partiendo el texto y colocando nuestro letra en la posicion que indiquemos
string = string[:5] + "k" + string[6:]
string 


def mutate_string(string, int, string_caracter):
    
    """Funcion para modificar una letra de una palabra""" 
    
    l = list(string)
    l[int] = string_caracter
    string = ''.join(l)
    
    return string

mutate_string("abracadabra", 5, "k")

    
