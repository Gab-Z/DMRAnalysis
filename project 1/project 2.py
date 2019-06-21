#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      anagh
#
# Created:     12/06/2019
# Copyright:   (c) anagh 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


df = pd.read_csv("C:\\python data files\dans-ma-rue.csv", sep = ';', header = 0 )
print( "df.shape retourne un tuple ( nb lignes, nb colonnes ) de la dataframe :"  )
print( df.shape )
print("---------------------------------------------------\n")
df10=df.head(10)
# df.head( n ) affiche les n 1ères lignes de la dataframe
print( "df100.head( n ) affiche les n 1ères lignes de la dataframe : " )
print( df10.head( 4 ) )
print("--------------------------------------------------\n")
print( "df.columns retourne un index des colonnes de la dataFrame" )
print( df10.columns )
print("---------------------------------------------------\n")
print( "df.dtypes retourne les noms de colonnes et les types de données quj'elles contiennent" )
print( df10.dtypes )
print("---------------------------------------------------\n")
# find min and max for dataframe
print(df["ANNEE DECLARATION"].min())
print(df["ANNEE DECLARATION"].max())
print("---------------------------------------------------\n")
print(df["TYPE"].min())
print(df["TYPE"].max())
print("---------------------------------------------------\n")
print(df.sort_values(by='ARRONDISSEMENT',ascending=0))
print("---------------------------------------------------\n")
print(df.pivot_table(df, index=['ANNEE DECLARATION','TYPE','ARRONDISSEMENT'], aggfunc='mean'))

plt.plot(df["TYPE"],df["ANNEE DECLARATION"])
plt.show()