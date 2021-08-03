# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 17:47:28 2021

@author: crf005r
"""
empty = ""

def look_for_key(main_box):
    
    pile=main_box.make_a_pile_to_look_through()
    
    while(pile is not empty):
        
        box=pile.grab_a_box()
        
        for item in box:
            if item.is_a_box():
                pile.append(item)
            elif item.is_a_key():
                print("found the key")

def look_for_key(box):
    for item in box:
        if item.is_a_box():
            look_for_key(item)
        elif item.is_a_key():
             print("found the key")
             
