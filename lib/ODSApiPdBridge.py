import requests
import pandas as pd
from pandas.io.json import json_normalize
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
import re


class ODSApiPdBridge() :


    '''
    La classe ODSApiPdBridge ( OpenDataSoft Api To Pandas Bridge )
    facilite les requêtes distantes vers un serveur opendatasoft
    et la conversion en objets Pandas
    '''

    responseFormats = ( "json", "csv" )
    apiVersions     = ( "1.0", "2.0" )
    urlRegEx        = re.compile( "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+" )
    datasetsColumns = {
        'datasetid' : {
            'enteteDeColonne' : 'datasetid'
        },
        'metas.title' : {
            'enteteDeColonne' : 'Jeu de données'
        },
        'metas.records_count' :{
            'enteteDeColonne' : 'Nb enregistrements'
        }
    }
    datasetsColumnsTitles = [ dc[ 'enteteDeColonne' ] for dc in datasetsColumns.values() ]

    def __init__( self, apiUrl = None, apiVersion = "1.0", responseFormat = "json" ) :

        if apiUrl != None :
            if apiUrl[ len( str( apiUrl ) ) - 4 :: ] == "api" :
                apiUrl += "/"
            if apiUrl[ len( str( apiUrl ) ) - 6 ::] != "/api/" :
                apiUrl += "/api/"

        # INITIALISATION DES PROPRIÉTÉS PRIVÉES
        self._private_apiUrl        = ""
        self._private_format        = ""
        self._private_apiVersion    = ""

        # AFFECTATION DES ARGUMENTS CONSTRUCTEUR AUX PROPRIÉTÉS PRIVÉES
        self.apiUrl         = apiUrl            # Correspond à '_private_apiUrl'
        self.format         = responseFormat    # Correspond à '_private_format'
        self.apiVersion     = apiVersion        # Correspond à '_private_apiVersion'

        # Vérification de la chaîne 'apiUrl' et ajout de '/api/' si nécessaire


    #########################################################
    # DÉFINITIONS DES GETTERS ET SETTERS
    #########################################################

    # PUBLIC : 'apiUrl' / PRIVÉ : '_private_apiUrl'
    @property
    def apiUrl( self ) :
        return self._private_apiUrl

    @apiUrl.setter
    def apiUrl( self, value ) :
        if value == None :
            self._private_apiUrl = None
        else :
            match = ODSApiPdBridge.urlRegEx.match( str( value ) )
            if match == None :
                raise ValueError(
                    ( "Erreur : la valeur affectée à la propriété 'apiUrl' : "
                      + "{valeurRecue} n'est pas une URL valide." ).format(
                        valeurRecue = str( value )
                    )
                )
            self._private_apiUrl = str( value )

    # PUBLIC : 'format' / PRIVÉ : '_private_format'
    @property
    def format( self ):
        return self._private_format

    @format.setter
    def format( self, value ) :
        if value not in ODSApiPdBridge.responseFormats :
            raise ValueError(
                (   "Erreur : la propriété 'format' passée à l'instance de "
                  + "ODSApiPdBridge est invalide. Accepté : {valeursAcceptees}. "
                  + "Reçu : {valeurRecue}").format(
                        valeursAcceptees = ", ".join(
                            ODSApiPdBridge.responseFormats
                        ),
                        valeurRecue      = str( value )
                  )
                 )
        self._private_format = value

    # PUBLIC : 'apiVersion' / PRIVÉ : '_private_apiVersion'
    @property
    def apiVersion( self ) :
        return self._private_apiVersion

    @apiVersion.setter
    def apiVersion( self, value ) :
        if value not in ODSApiPdBridge.apiVersions :
            raise ValueError(
                ( "Erreur : la valeur affectée à la propriété 'apiVersion' "
                  + "d'ODSApiPdBridge: {valeurRecue} est invalide. "
                  + "Accepété : {valeursAcceptees}" ).format(
                        valeurRecue = str( value ),
                        valeursAcceptees = ", ".join(
                            ODSApiPdBridge.apiVersions
                        )
                )
            )
        self._private_apiVersion = value

    #########################################################
    # FIN DES DÉFINITIONS DES GETTERS ET SETTERS
    #########################################################

    def get( self, _apiEntry , _apiTool, _params = None ) :
        if type( _params ) == dict :
            return  requests.get(
                        "{apiUrl}{apiEntry}/{apiVersion}/{apiTool}".format(
                            apiUrl      = self.apiUrl,
                            apiEntry    = _apiEntry,
                            apiVersion  = self.apiVersion,
                            apiTool     = _apiTool
                        ),params = _params
            )
        else :
            return  requests.get(
                        "{apiUrl}{apiEntry}/{apiVersion}/{apiTool}".format(
                            apiUrl      = self.apiUrl,
                            apiEntry    = _apiEntry,
                            apiVersion  = self.apiVersion,
                            apiTool     = _apiTool
                        )
                    )

    def csvFormatToDf( self, csv, sep = ";" ) :
        return pd.read_csv( StringIO( csv.text ), sep = sep )


    def jsonFormatToDf( self, json, recordsKey = None ) :
        if type( recordsKey ) == str :
            return json_normalize( json.json()[ recordsKey ] )
        else :
            return json_normalize( json.json() )


    def convertToDfByFormat(    self, format = None, sep = ";",
                                recordsKey = None, data = None  ) :
        frmt = format if format != None else self.format
        if frmt == "csv" :
            return self.csvFormatToDf( csv = data, sep = sep )
        elif frmt == "json" :
            return self.jsonFormatToDf( json = data, recordsKey = recordsKey )


    def getNbDatasets( self ) :
        req = self.get( _apiEntry   = "datasets",
                        _apiTool    = "search",
                        _params     =   {
                          "format"   : "json",
                          "rows"     : "0"
                        }
        )
        return req.json()[ "nhits" ]


    def getDatasets(    self, start = 0, rows = 10, format = None,
                        sep = ";", raw = False ) :

        frmt = format if format != None else self.format
        data = self.get(
            _apiEntry   =   "datasets",
            _apiTool    =   "search",
            _params     =   {
                "format"  : str( frmt ),
                "rows"    : str( rows ),
                "start"   : str( start )
            }
        )
        if raw == False :
            '''
            return self.convertToDfByFormat(
                data    = data,
                format  = frmt,
                sep     = sep
            )
            '''
            return json_normalize(  data = data.json()[ "datasets" ],
                                    #record_path = ["datasetid", "has_records"]
                                    meta = "metas"

            )

        else :
            if frmt == "csv" :
                return data.text
            elif frmt == "json" :
                return data.json()


    def getDatasetsInfo( self, start = 0, rows = 10 ) :
        if rows == "all" :
            rows = int( self.getNbDatasets() )
        df = self.getDatasets(
            start = start,
            rows = rows )[ ODSApiPdBridge.datasetsColumns.keys() ]
        df.columns = ODSApiPdBridge.datasetsColumnsTitles
        return df


    def getRecords( self, dataset, start = 0, rows = 10, format = None,
                    sep = ";", recordsKey = None, params = {}, raw = False ) :

        frmt = format if format != None else self.format
        parametres = {
            "dataset" : dataset,
            "start"   : str( start ),
            "rows"    : str( rows ),
            "format"  : frmt
        }

        for k in params.keys() :
            parametres[ k ] = str( params[ k ] )

        data = self.get(
            _apiEntry   =   "records",
            _apiTool    =   "search",
            _params     =   parametres
        )

        if raw == False :
            return self.convertToDfByFormat(
                format      = frmt,
                sep         = sep,
                recordsKey  = recordsKey,
                data        = data
            )
        else :
            if frmt == "csv" :
                return data.text
            elif frmt == "json" :
                return data.json()
