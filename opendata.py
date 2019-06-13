'''
requests needs to be installed :
pip install requests
'''

import requests
import json
import pandas as pd
from pandas.io.json import json_normalize

#url = 'https://opendata.paris.fr/api/records/1.0/search/?dataset=dans-ma-rue&sort=type&facet=type&facet=soustype&facet=code_postal&facet=ville&facet=arrondissement&facet=anneedecl&facet=prefixe&facet=intervenant&facet=conseilquartier'
url = 'https://opendata.paris.fr/api/records/1.0/search/'
requestParams = {
    "dataset" : "dans-ma-rue",
    "sort" : "type",
    "facet" : [ "type", "soustype", "code_postal", "ville", "arrondissement", "anneedecl", "prefixe", "intervenant", "conseilquartier" ]

}

urlData = requests.get( url, params = requestParams )

jsn =  urlData.json()

print( [ k for k in jsn.keys() ] )
df = pd.DataFrame.from_dict( urlData.json()[ "records" ] )
#df = pd.read_csv( io.StringIO( urlData.decode( 'utf-8' ) ) )
#urllib.request.urlopen('https://opendata.paris.fr/api/records/1.0/search/?dataset=dans-ma-rue&sort=type&facet=type&facet=soustype&facet=code_postal&facet=ville&facet=arrondissement&facet=anneedecl&facet=prefixe&facet=intervenant&facet=conseilquartier')
#r = requests.get('https://opendata.paris.fr/api/records/1.0/search/?dataset=dans-ma-rue&sort=type&facet=type&facet=soustype&facet=code_postal&facet=ville&facet=arrondissement&facet=anneedecl&facet=prefixe&facet=intervenant&facet=conseilquartier')

#print( r.headers['content-type'] )
#print( r.encoding )


#df = pd.read_csv( "heart.txt", sep = '\t', header = 0 )
#r.json()
#print( df.shape )

#print( df.head( 4 ) )

print( df.columns )
