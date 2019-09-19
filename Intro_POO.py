#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 21:05:13 2019

@author: carlos
"""

#Clase Restaurante
class Restaurante():

    #Atributos
    def __init__(self,nombre_restaurante,tipo_cocina):
        self.nombre_restaurante = nombre_restaurante
        self.tipo_cocina = tipo_cocina
        
    def describe_restaurant(self):
        print("El nombre del Restaurante es : " + self.nombre_restaurante)
        print("Tipo de comida : " + self.tipo_cocina)
        
    def open_restaurat(self):
        print("El Restaurante " + self.nombre_restaurante + " tiene un horario de 9 am a 5 pm")

    
        
Fonda = Restaurante('Gaby','Comida Corrida')
Fonda.describe_restaurant()
Fonda.open_restaurat()

Pizzas = Restaurante('Dominos','Pizzas')
Pizzas.describe_restaurant()
Tienda = Restaurante('Oxxo','Convini')
Tienda.describe_restaurant()

#Clase persona

class Persona():
    #Atributos
    def __init__(self,Primer_nombre, Apellido, edad,altura):
        self.Primer_nombre = Primer_nombre
        self.Apellido = Apellido
        self.edad = edad
        self.altura = altura
        
    def descripcion(self):
        print("Nombre : " + self.Primer_nombre + " " + self.Apellido + ", edad : " +  str(self.edad) + " , altura : " + str(self.altura))
    
    #Metodos
    def mensaje(self):
        
        if self.edad < 18:
            
            if self.altura < 1.70:
                print("Hola " + self.Primer_nombre + " , a un eres menor de edad , " + "con estatura baja")
            else:
                print("Hola " + self.Primer_nombre + " , a un eres menor de edad , " + "con estatura alta")
            
        else:
            if self.altura < 1.70 :
                print("Hola " + self.Primer_nombre + " , eres mayor de edad , " + "con estatura baja para tu edad")
            else:
                print("Hola " + self.Primer_nombre + " , eres mayor de edad , " + "buena estatura")
        

persona_0 = Persona('Carlos','Flores',27,1.60)
persona_0.descripcion()
persona_0.mensaje()





