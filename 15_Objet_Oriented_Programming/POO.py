# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 12:16:21 2022

@author: Maste
"""

#Clase

class Auto:
    
    marca = ""
    modelo = 2004
    placa = ""
    
taxi = Auto()

taxi.modelo

class nombre:
    pass

#Pertenecen a la clase nombre
carlos = nombre()
maria = nombre()

#sus atributos son : objeto.atributo = valor

carlos.edad = 30
carlos.sexo = 'masculino'
carlos.pais = 'bolivia'

maria.edad = 29
maria.sexo = 'femenino'
maria.pais = 'mexico'

#Métodos

class Matematicas:
    def suma(self):
        self.n1 = 2
        self.n2 = 3
        
s = Matematicas()    
s.suma()
print(s.n1 + s.n2)

class Ropa:
    
    def __init__(self):
        """Atributos"""
        self.marca = 'willow'
        self.talla = 'M'
        self.color = 'rojo'
        self.pais = 'China'

chamarra = Ropa()
chamarra.marca = 'Zara'
chamarra.talla = 'G'
chamarra.color = 'negro'

chamarra.__dict__

#Funciones para atributos
getattr(chamarra, 'marca') #Extraccion dato del atributo
getattr(chamarra, 'talla')
getattr(chamarra, 'color')

hasattr(chamarra, 'marca') #Validacion de atributos en una clase
hasattr(chamarra, 'tienda')

setattr(chamarra, 'marca', 'Aeropostal') #Cambio de valor de un atributo

delattr(chamarra, 'pais') #Elimina atributo

class Calculadora:
    def __init__(self, n1, n2):
        self.suma = n1 + n2
        self.resta = n1 - n2
        self.producto = n1 * n2
        self.division = n1 / n2
        
operacion = Calculadora(2,3)
operacion.suma
operacion.resta
operacion.producto
operacion.division

#Metodo constructor
class Persona:

    def __init__(self, nombre, año):
        self.nombre = nombre
        self.año = año
        
    def descripcion(self):
        return '{} tiene {} '.format(self.nombre, self.año)

    def comentario(self, frase):
        return '{} dice {} '.format(self.nombre, frase)

doctor = Persona('Charly', 29)
doctor.__dict__
doctor.descripcion()
doctor.comentario('Hola, en que puedo ayudarte.')

class Email:
    
    def __init__(self):
        self.enviado = False
    
    def enviar_correo(self):
        self.enviado = True

mi_correo = Email()
mi_correo.__dict__
print(mi_correo.enviar_correo())

##########
#Herencia#
##########

#Consiste en la posibilidad de crear una nueva clase apartir de una o más clases existentes.

class pokemon:
    pass
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo
        
    def descripcion(self):
        return '{} es un pokemon de tipo : {}'.format(self.nombre, self.tipo)
            
class pikachu(pokemon):
    
    def ataque(self, tipoataque):
        return '{} tipo de ataque : {}'.format(self.nombre, tipoataque)
    
class charmander(pokemon):
    
    def ataque(self, tipoataque):
        return '{} tipo de ataque : {}'.format(self.nombre, tipoataque)
    
nuevo_pokemon = pikachu('boby', 'electrico')
nuevo_pokemon.__dict__
nuevo_pokemon.descripcion()
    



    
        
        
        
        
        
        
        
        
        
        



