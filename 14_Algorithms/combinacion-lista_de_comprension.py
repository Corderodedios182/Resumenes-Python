# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#Ejemplos de listas de comprension
[x for x in range(10)]

[[x,y] for x in [1,2,3] for y in [2,3,4]]

[x for x in range(10) if x % 3 == 0]

[[x,y,z] for x in [1,2] for y in [1] for z in [2]]

#Combinacion de numeros for tradicional
x = 0
y = 0
z = 0
n = 2
l = list()

for i in range(x+1):
    for j in range(y+1):
        for k in range(z+1):
            if (i+j+k != n):
                l.append([i,j,k])
    print(l)
        
#Combinacion de numeros con listas de comprension
a, b, c, n = [int(input()) for _ in range(4)]

[[x,y,z] for x in range(a + 1) for y in range(b + 1) for z in range(c + 1) if x + y + z != n]
