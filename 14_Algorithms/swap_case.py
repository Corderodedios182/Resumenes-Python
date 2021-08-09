# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 17:33:52 2021

@author: crf005r
"""

def swap_case(string):
    
    """Convirte minusculas en mayusculas y viceversa"""
    
    l = []
    
    for i in range(len(list(string))):

        if string[i].islower() == True:
            
            l.append(string[i].upper())
            
        else:
            
            l.append(string[i].lower())
        
    string = ''.join(l)
    
    return string
        