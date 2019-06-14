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

arr =  [ ( d["x"]["year"], d["my_count"] ) for d in jsn ]
annees = [ e[ 0 ] for e in arr ]
totaux = [ e[ 1 ] for e in arr ]
print(totaux)

df = pd.DataFrame.from_records( arr, columns=[ "Année", "Total d'anomalies signalées" ])
ticky = max( totaux ) / 10

#print(df)
#df.hist( column = "Année" )

#counts, bins = np.array(totaux)
counts, bins = np.histogram(totaux, bins=10)
plt.hist(bins[:-1], bins, weights=counts)
#plt.yticks( [ t * ticky for t in range( 10 ) ] )
plt.title("histogram")
plt.show()
'''

plt.xlabel('x label')
plt.ylabel('y label')

plt.title("Simple Plot")

plt.legend()
npHist = np.histogram(totaux, bins=10)
n, bins, patches = plt.hist( totaux, 10, facecolor='blue', alpha=0.5 )
plt.show()
'''
