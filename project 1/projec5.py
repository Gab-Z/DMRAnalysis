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
df10000=df.head(10000)
#arrondissement=df.groupby(["ARRONDISSEMENT","ANNEE DECLARATION","TYPE"]).size()
#print(df.groupby(["ARRONDISSEMENT","ANNEE DECLARATION","TYPE"]).count())
#print(df.groupby(["MOIS DECLARATION","ANNEE DECLARATION"]).count())
#print(df.groupby("ANNEE DECLARATION").count())
#print(df.groupby("MOIS DECLARATION").count())
#print(df.groupby(["ARRONDISSEMENT","ANNEE DECLARATION"]).size())

# Tri les annomalie par arrondissement et par annee
def Arrond_et_annee(df):
  arrondissement=df.groupby(["ARRONDISSEMENT","ANNEE DECLARATION","TYPE"]).size()
  return arrondissement

# Tri les annomalie par arrondissement et par mois
def Arrond_et_mois(df):
  mois=df.groupby(["ARRONDISSEMENT","MOIS DECLARATION","TYPE"]).size()
  return mois

# Tri les annomalie par arrondissement et par type
def Arrond_et_type(df):
  TYPE=df.groupby(["ARRONDISSEMENT","TYPE","SOUSTYPE"]).size()
  return TYPE

def max_Arrond_et_annee(df):
    pivot = df10000.pivot_table(index=['ARRONDISSEMENT'], values=['ANNEE DECLARATION','TYPE'], aggfunc='max')
    return pivot

def min_Arrond_et_annee(df):
    pivot = df10000.pivot_table(index=['ARRONDISSEMENT'], values=['ANNEE DECLARATION','TYPE'], aggfunc='min')
    return pivot

def max_Arrond_et_mois(df):
    pivot = df10000.pivot_table(index=['ARRONDISSEMENT'], values=['MOIS DECLARATION','TYPE'], aggfunc='max')
    return pivot

def min_Arrond_et_mois(df):
    pivot = df10000.pivot_table(index=['ARRONDISSEMENT'], values=['MOIS DECLARATION','TYPE'], aggfunc='min')
    return pivot

def max_Arrond_et_type(df):
    pivot = df10000.pivot_table(index=['ARRONDISSEMENT'], values=['TYPE','SOUSTYPE'], aggfunc='max')
    return pivot

def min_Arrond_et_type(df):
    pivot = df10000.pivot_table(index=['ARRONDISSEMENT'], values=['TYPE','SOUSTYPE'], aggfunc='min')
    return pivot

arrAnne = Arrond_et_annee(df)
print((Arrond_et_annee)(df))
print("------------------------------------------------------------------------------------")
print((Arrond_et_mois)(df))
print("------------------------------------------------------------------------------------")
print((Arrond_et_type)(df))
print("------------------------------------------------------------------------------------")
print(max_Arrond_et_annee(df10000))
print((min_Arrond_et_annee)(df10000))
print(max_Arrond_et_mois(df10000))
print((min_Arrond_et_mois)(df10000))
print(max_Arrond_et_type(df10000))
print((min_Arrond_et_type)(df10000))
#plt.plot(arrAnne)
#plt.show()
