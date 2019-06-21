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

df = pd.read_csv("C:\\python data files\dans-ma-rue.csv", sep = ';', header = 0 )
print( "df.shape retourne un tuple ( nb lignes, nb colonnes ) de la dataframe :"  )
#arrondissement=df.groupby(["ARRONDISSEMENT","ANNEE DECLARATION","TYPE"]).size()
#print(df.groupby(["ARRONDISSEMENT","ANNEE DECLARATION","TYPE"]).count())
#print(df.groupby(["MOIS DECLARATION","ANNEE DECLARATION"]).count())
#print(df.groupby("ANNEE DECLARATION").count())
#print(df.groupby("MOIS DECLARATION").count())
#print(df.groupby(["ARRONDISSEMENT","ANNEE DECLARATION"]).size())

# Tri les annomalie par arrondissement et par annee
def Arrond_et_annee(df):
  arrondissement_size=df.groupby(["ARRONDISSEMENT","ANNEE DECLARATION","TYPE"]).size()
  return arrondissement_size
  arrondissement_min=df.groupby(["ARRONDISSEMENT","ANNEE DECLARATION","TYPE"]).min()
  return arrondissement_min


# Tri les annomalie par arrondissement et par mois
def Arrond_et_mois(df):
  mois=df.groupby(["ARRONDISSEMENT","MOIS DECLARATION","TYPE"]).size()
  return mois

# Tri les annomalie par arrondissement et par type
def Arrond_et_type(df):
  TYPE=df.groupby(["ARRONDISSEMENT","MOIS DECLARATION","TYPE","SOUSTYPE"]).size()
  return TYPE

print((Arrond_et_annee)(df))
#print("------------------------------------------------------------------------------------")
#print((Arrond_et_mois)(df))
#print("------------------------------------------------------------------------------------")
#print((Arrond_et_type)(df))
#print("------------------------------------------------------------------------------------")

