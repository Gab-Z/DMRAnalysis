import matplotlib.pyplot as plt
import numpy as np

import requests
import json
import pandas as pd
from pandas.io.json import json_normalize

#url = 'https://opendata.paris.fr/api/records/1.0/search/?dataset=dans-ma-rue&sort=type&facet=type&facet=soustype&facet=code_postal&facet=ville&facet=arrondissement&facet=anneedecl&facet=prefixe&facet=intervenant&facet=conseilquartier'
#urlSearch =     'https://opendata.paris.fr/api/records/1.0/search/'
urlAnalysis =   'https://opendata.paris.fr/api/records/1.0/analyze/'
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
    "dataset" : "dans-ma-rue",
    "x" : "anneedecl",
    "y.my_count.func" : "COUNT"
}


#urlData = requests.get( url, params = requestParams )
urlData = requests.get( urlAnalysis, params = requestParamsAnalysis )
jsn = urlData.json()
print(jsn)

plt.plot( [ d["x"]["year"] for d in jsn ],  [ d["my_count"] for d in jsn ], label='linear')

plt.xlabel('x label')
plt.ylabel('y label')

plt.title("Simple Plot")

plt.legend()

plt.show()
