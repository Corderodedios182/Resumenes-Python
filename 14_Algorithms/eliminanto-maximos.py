#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 18:36:22 2021

Removiendo los maximos de una lista

@author: Charly
"""

calificaciones = [2,3,3,4,5,6,6,7,7,7]

a = max(calificaciones)

c = calificaciones.count(a)

for i in range(c):
    calificaciones.remove(a)

print(max(calificaciones))
