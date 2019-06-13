#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Administrateur
#
# Created:     12/06/2019
# Copyright:   (c) Administrateur 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()

import numpy as np
import math
import pandas
import matplotlib
import matplotlib.pyplot as plt


df=pandas.read_csv("dans-ma-rue.csv", sep='\t', delimiter=';',  header=0)
x = [1, 2, 2, 3, 4, 4, 4, 4, 4, 5, 5]


plt.xticks(range(5), [2012,2013,2014,2015,2016,2017,2018], rotation = 45)
plt.yticks(range(23),[1,2,3,4,5,6])
plt.xlabel('Année')
plt.ylabel('Numero Arrondissement')

plt.show()
print(df.columns)