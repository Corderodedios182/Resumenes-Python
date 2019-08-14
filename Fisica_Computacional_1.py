# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.

Descripcion:
    Expresion de la ecuacion de onda 
"""

from math import sqrt, tan

#Variables

V0 = 20
a = 2./197
m = 938
x =10

def Energia_Onda(x):

    return sqrt(2*m*(V0-abs(x)))*(1./tan(sqrt(2*m*a*a*(V0-abs(x)))))+sqrt(2*m*abs(x))
    
#Tolerancia que damos
tol = 1e-5

xa = 1.5
xb = 2.1

fa = Energia_Onda(xa)
fb = Energia_Onda(xb)


while abs(xa-xb) > tol:
    xm = (xa+xb)/2.
    fm = Energia_Onda(xm)
    if fa * fm < 0:
        xb = xm
    if fm * fb < 0:
        xa = xm
        
print("La raiz es:", xm)
print(Energia_Onda(xm))






