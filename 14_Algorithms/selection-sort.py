# -*- coding: utf-8 -*-
"""

@author: crf005r

"""

arr = [120,134,24,43,54,213,1]

def findSmallest(arr):
    """Look for the smallest element"""
    smallest = arr[0]
    smallest_index = 0
    
    for i in range(1, len(arr)):
        if arr[i] < smallest:
            smallest = arr[i]
            smallest_index = i
            
    return smallest_index

def selectionSort(arr):
    """Sorting algorithm by selection
        Big O notation equal O(n x n)
    """
    newArr = []
    
    for i in range(len(arr)):
        smallest = findSmallest(arr) #Stores the smallest value
        newArr.append(arr.pop(smallest)) #Stores the index of the smallest value
    
    return newArr

findSmallest(arr)

selectionSort(arr)
