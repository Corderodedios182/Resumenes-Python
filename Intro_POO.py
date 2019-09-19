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
        #Atributo que ayuda al metodo Genero
        self.distancia = 0
        
    def descripcion(self):
        
        print("Nombre : " + self.Primer_nombre + " " + self.Apellido + ", edad : " +  str(self.edad) + " , altura : " + str(self.altura))
        
    def Correr(self):
        
        print("Has recorrido : " + str(self.distancia) + " metros ")
        
    #Adicionalmente podemos meter logica para crear respuestas personalizadas
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
        

#Tenemos parametros obligatorios para poder definir la clases adecuadamente
persona_0 = Persona('Carlos','Flores',27,1.60)
persona_0.descripcion()
#Metodo que contiene un mensaje personalizado
persona_0.mensaje()

#¿Que sucede con un metodo que tiene atributos dinamicos?
#Primero arrojara el valor preterminado que colocamos
persona_0.distancia
#Existen varias maneras de cambiar el valor del atributo y metodo
#1. Podemos asignarle directamente un valor al atributo 
persona_0.distancia = 10 
#Y el metodo habra actualizado el valor
persona_0.Correr()


#Pero si quisieramos cambiar los valores mediante el metodo.

class Persona():
    #Atributos
    def __init__(self,Primer_nombre, Apellido, edad,altura):
        self.Primer_nombre = Primer_nombre
        self.Apellido = Apellido
        self.edad = edad
        self.altura = altura
        #Atributo que ayuda al metodo Genero
        self.distancia = 0
        
    def descripcion(self):
        print("Nombre : " + self.Primer_nombre + " " + self.Apellido + ", edad : " +  str(self.edad) + " , altura : " + str(self.altura))
        
    def Correr(self, distancia):
        self.distancia = distancia
        print("Has recorrido : " + str(self.distancia))

persona_0 = Persona('Carlos','Flores',27,1.60)
persona_0.descripcion()
persona_0.distancia #Ya podemos colocar el valor directo en el metodo para que haga el cambio
persona_0.Correr(100)
persona_0.distancia #Ha sido actualizado por medio del metodo


#Supongamos que necesitamos sumar la distancia que corremos, y cada que ocupemos el metodo Correr automaticamente se sumara al atributo distancia


class Persona():
    #Atributos
    def __init__(self,Primer_nombre, Apellido, edad,altura):
        self.Primer_nombre = Primer_nombre
        self.Apellido = Apellido
        self.edad = edad
        self.altura = altura
        #Atributo que ayuda al metodo Genero
        self.distancia = 0
        
    def descripcion(self):
        print("Nombre : " + self.Primer_nombre + " " + self.Apellido + ", edad : " +  str(self.edad) + " , altura : " + str(self.altura))
        
    def Correr(self, distancia): 
        self.distancia += distancia #Observa como el parametro se actualiza solo
        print("Has recorrido : " + str(self.distancia))
        
        
persona_0 = Persona('Carlos','Flores',27,1.60)
persona_0.descripcion()
persona_0.distancia #Ya podemos colocar el valor directo en el metodo para que haga el cambio
persona_0.Correr(40)
persona_0.distancia #Ha sido actualizado por medio del metodo
        
persona_0.suma_recorrido(20)
persona_0.distancia


#Modifiquemos la clase Restaurante

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


    
    
    
    
    
    
    
    






