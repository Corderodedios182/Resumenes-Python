# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 14:47:59 2021

@author: crf005r
"""
import math as math
from math import log

# Binary search algorithm

def binary_search(list, item):
    #low and high keep track of which part of the list you’ll search in.
    low = 0
    high = len(list) - 1
    
    while low <= high: # While you haven’t narrowed it down to one element
        mid = (low + high) # check the middle element
        guess = list[mid]
        if guess == item: #Found the item
            return mid
        if guess > item: # The guess was too high.
            high = mid - 1
        else: #The guess was too low.
            low = mid + 1
    return None #The item doesn´t exist


# Program to display the Fibonacci sequence up to n-th term

def Fibonacci(nterms):
    
    fibonacci_list = []
    
    # first two terms
    n1, n2 = 0, 1
    count = 0
    
    # check if the number of terms is valid
    if nterms <= 0:
       print("Please enter a positive integer")
    # if there is only one term, return n1
    elif nterms == 1:
       print("Fibonacci sequence upto",nterms,":")
       print(n1)
    # generate fibonacci sequence
    else:
       print("Fibonacci sequence:")
       while count < nterms:
           print(n1)
           nth = n1 + n2
           # add fibonacci term
           fibonacci_list.append(nth)
           # update values
           n1 = n2
           n2 = nth
           count += 1
           
    return fibonacci_list

#Creation of n elements of the Fibonacci sequence       
my_list = Fibonacci(100) 

#Search for element x in the Fibonacci sequence
binary_search(my_list,89)
binary_search(my_list,514229)

# Computational complexity in binary search algorithm
math.log2(100)
math.log2(240000)

#Exercises:
    
#Suppose you have a sorted list of 128 names, and you're searching
#through it using binary search. What’s the maximum number of
#steps it would take?

math.log2(128)

#Suppose you double the size of the list. What’s the maximum
#number of steps now?

math.log2(128*2)
