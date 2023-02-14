# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 16:50:56 2023

@author: Wojtek

ASSUMPTION:
    !!!!
    DANE SA POSORTOWANE ROSNACO 



"""

import numpy as np
import pandas as pd

np.random.seed(123)

data = (np.random.uniform(1,5,[49]))
data = np.sort(data)
data_zaokr = np.round(data)

print(f'DANE WEJSCIOWE: \n{data}\n')
print(f'DANE ZAOKRAGLONE: \n{data_zaokr}\n')
test = np.unique(data_zaokr, return_counts=True)
liczby, powtorzenia = test
for liczba, count in zip(liczby, powtorzenia):
    print(f"{liczba}: ilosc powtorzen: {count}")
    
    
def flatten_distribution(array,label_num=5):
    '''
    data
    data_zaokr
    
    bucketuj to do rownych 
    BIORE ILOSC DZIELE PRZEZ 5
    '''
    arr_len = len(array)
    number_in_label = arr_len//5
    reszta = arr_len%5
    #print(number_in_label)
    #print(arr_len)
    #print(reszta)
    labels = []
    for i in range(1,label_num+1):
        for j in range(number_in_label):
            labels.append(i)
    for k in range(reszta):
        labels.append(i) # BO I ZOSTALO JAKO NAJWYZZY LABEL !!
    return labels

labels = flatten_distribution(data)
print(labels)