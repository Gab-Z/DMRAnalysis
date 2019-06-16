import matplotlib.pyplot as plt
import numpy as np

import requests
import json
import pandas as pd
from pandas.io.json import json_normalize

import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

################
#Quelles années a été le plus / moins anomalies signalées  par  arrondissement de Paris?
##########################



#url = 'https://opendata.paris.fr/api/records/1.0/search/?dataset=dans-ma-rue&sort=type&facet=type&facet=soustype&facet=code_postal&facet=ville&facet=arrondissement&facet=anneedecl&facet=prefixe&facet=intervenant&facet=conseilquartier'
#urlSearch =     'https://opendata.paris.fr/api/records/1.0/search/'
'''
https://examples.opendatasoft.com/api/datasets/1.0/search?refine.language=en&refine.modified=2017/10
https://examples.opendatasoft.com/api/datasets/1.0/search?exclude.publisher=UNESCO&sort=-modified

'''
urlAnalysis =   'https://opendata.paris.fr/api/datasets/1.0/search/'
'''
requestParams = {
    "dataset" : "dans-ma-rue",
    "sort" : "type",
    "rows" : 2000,
    "facet" : [ "type", "anneedecl" ]
    #"facet" : [ "type", "soustype", "code_postal", "ville", "arrondissement", "anneedecl", "prefixe", "intervenant", "conseilquartier" ]
}
'''
requestParamsAnalysis = {
    "format" : "csv",
    "rows" : "2",
    "fields":"datasetid"
}


#urlData = requests.get( url, params = requestParams )
urlData = requests.get( urlAnalysis, params = requestParamsAnalysis )
print( urlData.text )
print( "" )
df = pd.read_csv( StringIO( urlData.text ), sep = ";" )
print( df[ "datasetid" ] )
#jsn = urlData.json()
#print(jsn)
'''
plt.plot( [ d["x"]["year"] for d in jsn ],  [ d["my_count"] for d in jsn ], label='linear')

plt.xlabel('x label')
plt.ylabel('y label')

plt.title("Simple Plot")

plt.legend()

plt.show()
'''
