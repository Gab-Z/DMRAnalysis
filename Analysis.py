#-------------------------------------------------------------------------------
# Name:        Analysis
# Purpose:
#
# Author:      Sébastien
#
# Created:     18/06/2019
# Copyright:   (c) Sébastien 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pandas

from tkinter import *

def main():
    pass

if __name__ == '__main__':
    main()


df=pandas.read_csv("dans-ma-rue.csv", sep='\t', delimiter=';', header=0)

fenetre = Tk()

canvas = Canvas(fenetre, width=800, height=450, bg='ivory')

def graphique1():
    canvas.delete("all")
    resultat1=df.groupby(['ARRONDISSEMENT','ANNEE DECLARATION']).size()
    print(resultat1)


def graphique2():
    canvas.delete("all")
    resultat2=df.groupby(['TYPE','MOIS DECLARATION']).size()
    print(resultat2)


def graphique3():
    canvas.delete("all")
    resultat3=df.groupby(['TYPE','ARRONDISSEMENT']).size()
    print(resultat3)


def initBoutons():
    bouton1 = Button(fenetre, text="Question 1", command=graphique1)
    bouton1.pack(padx = 5, pady = 5)
    bouton2 = Button(fenetre, text="Question 2", command=graphique2)
    bouton2.pack(padx = 5, pady = 5)
    bouton3 = Button(fenetre, text="Question 3", command=graphique3)
    bouton3.pack(padx = 5, pady = 5)

    bouton0 = Button(fenetre, text="Quitter", command=fenetre.destroy)
    bouton0.pack(padx = 5, pady = 5)


canvas.pack(side=RIGHT, padx=3, pady=3)

initBoutons()

fenetre.mainloop()
