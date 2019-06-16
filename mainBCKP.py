
from pprint import pprint
from ODSApiPdBridge import ODSApiPdBridge

bridge = ODSApiPdBridge( apiUrl = 'https://opendata.paris.fr' )

print( bridge.apiUrl )
#print( bridge.getNbDatasets() )
dtsts = bridge.getDatasetsInfo( rows = bridge.getNbDatasets() )
pprint( dtsts )


'''
pprint  ( bridge.getRecords(
            dataset = "les-arbres",
            start = 0,
            rows = 1,
            format = "json",
            recordsKey = "records",
            #params = { "fields" : "corps"},
            raw = True
        )
)
'''
