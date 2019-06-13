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

def main():
    pass

if __name__ == '__main__':
    main()
import pandas as pd
import numpy as np

# import du fichier heart.txt avec pandas dans la variable df (df = DataFrame)
df = pd.read_csv("C:\\python data files\dans-ma-rue.csv", sep = ';', header = 0 )
print(df.shape)
df50=df.head(50)
print(df50)
print(df50.columns)
#print(df.dtypes)
#print(df.columns.values)
print(df50[['TYPE']])
count = df50['TYPE'].value_counts()
print(count)

#print( type( df[ ['TYPE' ,'SOUSTYPE' ] ] ))

