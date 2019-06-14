import matplotlib.pyplot as plt
import numpy as np

import requests
import json
import pandas as pd
from pandas.io.json import json_normalize

#url = 'https://opendata.paris.fr/api/records/1.0/search/?dataset=dans-ma-rue&sort=type&facet=type&facet=soustype&facet=code_postal&facet=ville&facet=arrondissement&facet=anneedecl&facet=prefixe&facet=intervenant&facet=conseilquartier'
url = 'https://opendata.paris.fr/api/records/1.0/search/'
requestParams = {
    "dataset" : "dans-ma-rue",
    "sort" : "type",
    "rows" : 2000,
    "facet" : [ "type", "anneedecl" ]
    #"facet" : [ "type", "soustype", "code_postal", "ville", "arrondissement", "anneedecl", "prefixe", "intervenant", "conseilquartier" ]

}

urlData = requests.get( url, params = requestParams )
jsn = urlData.json()
df = json_normalize( jsn[ "records" ] )

subDf = df.groupby( "fields.anneedecl" )[ "fields.arrondissement" ].count()
print( subDf )
print("#############################")
print( subDf.keys() )#
#print( subDf[ "fields.anneedecl" ].values )
df_asarray = subDf.values
df_asArrayHeads = subDf.index



print( df_asarray )
plt.plot( df_asArrayHeads, df_asarray, label='linear')

plt.xlabel('x label')
plt.ylabel('y label')

plt.title("Simple Plot")

plt.legend()

plt.show()
