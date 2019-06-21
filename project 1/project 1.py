-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      anagh
#
# Created:     12/06/2019
# Copyright:   (c) anagh 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()
import pandas as pd
import numpy as np



# import du fichier heart.txt avec pandas dans la variable df (df = DataFrame)
df = pd.read_csv("C:\\python data files\dans-ma-rue.csv", sep = ';', header = 0 )
print(df.shape)
df100=df.head(100)

print(df100)
print(df100.columns)
#print(df.dtypes)
#print(df.columns.values)

count = df100['TYPE']
print(count)
print(count.iloc)
list_type=df100['TYPE'].tolist()
print("list_type:",list_type)
print("---------------------------------------------------\n")
count1 = df100['MOIS DECLARATION']
list_soustype=df100['MOIS DECLARATION'].tolist()
print("list_MOIS DECLARATION:",list_soustype)
print("---------------------------------------------------\n")
count2 = df100['ARRONDISSEMENT']
list_arrondissement=df100['ARRONDISSEMENT'].tolist()
print("list_arrondissement:",list_arrondissement)

print("les annomaliees signalees par arrondissement de paris")


