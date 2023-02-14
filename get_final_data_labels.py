# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 16:35:31 2023


ASSUMPTION:
    !!!!
    DANE SA POSORTOWANE ROSNACO 

@author: Wojtek
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel('przerobione_recznie_ankieta.xlsx')
# Zapisz od 6 do 8 jako odzielny df
df_6_8 = df[df['Zaokraglone'] > 5]
df_1_5 = df[df['Zaokraglone'] < 6]

# sortuj po sredniej rosnaco ! WAZNE
df_1_5 = df_1_5.sort_values("Srednia")
print(df_1_5)

#print(df_1_5.columns)



def get_distribution(df,column_name="Zaokraglone"):
    '''
    Plots distribution from given Dataframe
    '''
    df[column_name] = df[column_name].astype(int)
    value_counts = df[column_name].value_counts()
    value_counts = value_counts.sort_index()
    print(value_counts)
    
    # KOLOWY
    value_counts.plot.pie(figsize=(5, 5), autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')  
    plt.show()
    
    # SLUPKOWY
    value_counts.plot.bar(figsize=(8, 5))
    plt.xlabel('Level')
    plt.ylabel('Counts')
    plt.show()

#get_distribution(df)
#get_distribution(df_1_5)


srednia_labels = df_1_5['Srednia'].to_numpy()

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

new_labels = flatten_distribution(srednia_labels)

df_1_5["New_labels"] = new_labels 

print(df_1_5)


get_distribution(df_1_5, column_name="New_labels")

#df_1_5.to_excel("SPRAWDZ.xlsx", index=False)

'''
TODO

POLACZ 1_5 z 6_8



'''