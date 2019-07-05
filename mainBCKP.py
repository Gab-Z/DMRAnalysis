
from pprint import pprint
from ODSApiPdBridge import ODSApiPdBridge

bridge = ODSApiPdBridge( apiUrl = 'https://opendata.paris.fr' )

print( bridge.apiUrl )
#print( bridge.getNbDatasets() )
dtsts = bridge.getDatasetsInfo( rows = bridge.getNbDatasets() )
