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
import os

dirPath = os.path.join(
    os.path.abspath(
        os.path.dirname( __file__ )
    ),
    'staticDataSheets'
)

from tkinter import *


df=pandas.read_csv(os.path.join( dirPath, "dans-ma-rue.csv" ), sep='\t', delimiter=';', header=0)

fenetre = Tk()
fenetre.title("Dans ma rue - Anomalies")

canvas_width = 1200
canvas_height = 600
canvas = Canvas(fenetre, width=canvas_width, height=canvas_height, bg='ivory')
canvas.pack(side=RIGHT)

#data2=df.groupby(['TYPE','MOIS DECLARATION']).TYPE.count()
#data3=df.groupby(['TYPE','ARRONDISSEMENT']).TYPE.count()

def graph1():

    data=df.groupby(['ARRONDISSEMENT','ANNEE DECLARATION']).TYPE.count()

    nbBarres = len(data)
    dataMax = max(data)

    cWidth = canvas[ 'width ']
    cHeight = canvas[ 'height' ]

    margeLateraleExt = cWidth * 0.05
    largeurDispo = cWidth - 2 * margeLateraleExt
    largeurContBaton = largeurDispo / nbBarres
    margesVerticalesExt = cHeight * 0.05
    hauteurDispo = cHeight - 2 * margesVerticalesExt
    ratioValeurs = hauteurDispo / dataMax

    couleursParAnnee = {
        '2012' : "blue",
        '2013' : "green",
        '2014' : "red",
        '2015' : "yellow",
        '2016' : "pink",
        '2017' : "brown",
        '2018' : 'orange'

    }

    index = 0

    for arrondissement_annee, valeur in data.items():
        canvas.create_rectangle(
            round(margeLateraleExt + largeurContBaton * index),
            round(cHeight - margesVerticalesExt),
            round(margeLateraleExt + largeurContBaton * index + largeurContBaton),
            round(cHeight - (margesVerticalesExt + valeur * ratioValeurs)),
            fill= couleursParAnnee[ str( arrondissement_annee[1] ) ]
        )


        index = index + 1


bouton1 = Button(fenetre, text="Task 1", command=graph1)
bouton1.pack(padx = 5, pady = 5)
#bouton2 = Button(fenetre, text="Task 2", command=graph2)
#bouton2.pack(padx = 5, pady = 5)
#bouton3 = Button(fenetre, text="Task 3", command=graph3)
#bouton3.pack(padx = 5, pady = 5)

bouton0 = Button(fenetre, text="Quit", command=fenetre.destroy)
bouton0.pack(padx = 5, pady = 5)


fenetre.mainloop()
