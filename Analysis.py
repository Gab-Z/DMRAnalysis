#-------------------------------------------------------------------------------
# Name:        Analysis
# Purpose:
#
# Author:      Sébastien
#
# Created:     12/06/2019
# Copyright:   (c) Sébastien 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pandas
import csv
import numpy as np
import matplotlib.pyplot as plt
import tkinter

def main():
    pass

if __name__ == '__main__':
    main()

df=pandas.read_csv("dans-ma-rue.csv", sep='\t', delimiter=';', header=0)

root = tkinter.Tk()

obj = tkinter.Label (text = "zone de texte")

obj.pack()

root.mainloop()



























