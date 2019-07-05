#-------------------------------------------------------------------------------
# Name:        Analysis GM
# Purpose:
#
# Author:      Sébastien
#
# Created:     21/06/2019
# Copyright:   (c) Sébastien 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pandas
import gmplot
import webbrowser

def afficherDispersionAnomalies( dataframe, start = 0, nbRows = 5000):

    #df=dataframe.head( 5000 )
    df = dataframe.loc[ start : start + nbRows ]
    geo_point_2d = df['geo_point_2d']

    gmap = gmplot.GoogleMapPlotter(48.853, 2.35, 12) # Centrage de la map

    latitude = []
    longitude = []

    for i in range( len( geo_point_2d ) ):
        sp = geo_point_2d[ i ].split( "," )
        latitude.append( float( sp[ 0 ] ) )
        longitude.append( float( sp[ 1 ] ) )

    gmap.heatmap( latitude, longitude )
    gmap.scatter( latitude, longitude, color = 'red', size = 25, marker = False ) # Affichage de la dispersion des anomalies

    #gmap.apikey = "AIzaSyBBEN-7KXwcqxB7E2UOlimJsSf6BezNPYY" # Utilisation de l'API key Google Maps
    gmap.draw( "map.html" ) # Création du lien html de la map
    webbrowser.open( "map.html" ) # Ouverture de la map dans le navigateur



#afficherDispersionAnomalies(coordonnees = geo_point_2d)









