import requests
import pandas as pd
from pandas.io.json import json_normalize
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
import re
import json
from pprint import pprint


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
        'metas.title' : {
            'enteteDeColonne' : 'Jeu de données',
            'sortPriority'    : 1
        },
        'metas.records_count' : {
            'enteteDeColonne' : 'Enregistrements'
        },
        'datasetid' : {
            'enteteDeColonne' : 'datasetid'
        },
        'metas.data_processed' : {
            'enteteDeColonne' : 'Modifié le'
        },
        'fields'               : {
            'enteteDeColonne' : 'Colonnes',
            'cléDesDictsMembres' : 'label'
        }
    }
    datasetsColumnsTitles = [ dc[ 'enteteDeColonne' ] for dc in datasetsColumns.values() ]

    class BadRequestResponse() :
        def __init__( self, code ) :
            self.code = code


    def __init__( self, apiUrls = None, apiVersion = "1.0", responseFormat = "json" ) :

        # INITIALISATION DES PROPRIÉTÉS PRIVÉES
        self._private_apiUrls        = []
        self._private_format        = ""
        self._private_apiVersion    = ""

        # AFFECTATION DES ARGUMENTS CONSTRUCTEUR AUX PROPRIÉTÉS PRIVÉES
        #self.apiUrls         = apiUrls            # Correspond à '_private_apiUrls'
        if apiUrls != None :
            self.addUrl( apiUrls )
        self.format         = responseFormat    # Correspond à '_private_format'
        self.apiVersion     = apiVersion        # Correspond à '_private_apiVersion'

    #########################################################
    # DÉFINITIONS DES GETTERS ET SETTERS
    #########################################################

    # PUBLIC : 'apiUrls' / PRIVÉ : '_private_apiUrls'
    @property
    def apiUrls( self ) :
        return self._private_apiUrls

    @apiUrls.setter
    def apiUrls( self, value ) :
        if value == None :
            self._private_apiUrls = None
        else :
            match = ODSApiPdBridge.urlRegEx.match( str( value ) )
            if match == None :
                raise ValueError(
                    ( "Erreur : la valeur affectée à la propriété 'apiUrls' : "
                      + "{valeurRecue} n'est pas une URL valide." ).format(
                        valeurRecue = str( value )
                    )
                )
            self._private_apiUrls = str( value )

    def addUrl( self, apiUrl ) :
        if type( apiUrl ) != list :
            apiUrl = [ apiUrl ]
        for url in apiUrl :
            if type( url ) != str :
                raise ValueError(
                    "Erreur : un élément passé à la méthode 'addUrl' ({}) "
                    + "n'est pas de type str".format( str( url ) )
                )
            if url[ len( str( url ) ) - 4 :: ] == "api" :
                url += "/"
            if url[ len( str( url ) ) - 6 ::] != "/api/" :
                url += "/api/"
            self.apiUrls.append( url )


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

    def getDatasetsColumnsTitle( self ) :
        return ODSApiPdBridge.datasetsColumnsTitles

    def getColumnSortingPriority( self ) :
        ret = []
        for k in ODSApiPdBridge.datasetsColumns.keys() :
            if 'sortPriority' in ODSApiPdBridge.datasetsColumns[ k ] :
                ret.append( ( ODSApiPdBridge.datasetsColumns[ k ][ 'sortPriority' ] , ODSApiPdBridge.datasetsColumns[ k ][ 'enteteDeColonne' ] ) )
        ret.sort( key = lambda tup: tup[ 0 ] )
        return [ t[ 1 ] for t in ret ]

    def get( self, apiUrl, apiEntry , apiTool, params = None ) :
        req = 0
        ret = None
        try :
            reqStr = "{apiUrl}{apiEntry}/{apiVersion}/{apiTool}".format(
                apiUrl     = apiUrl,
                apiEntry    = apiEntry,
                apiVersion  = self.apiVersion,
                apiTool     = apiTool
            )
            reqDict = { 'stream' : True }
            if type( params ) == dict :
                reqDict[ 'params' ] = params

            with requests.get(
                reqStr,
                **reqDict
            ) as req :
                for chunk in req.iter_content(
                    chunk_size = 256,
                    decode_unicode = True
                ) :
                    if chunk: # filter out keep-alive new chunks
                        if ret == None :
                            ret = chunk
                        else :
                            ret = ret + chunk
            if str( req.status_code ) == "200":
                return json.loads( ret )
            else :
                return ODSApiPdBridge.BadRequestResponse( code = req.status_code )
        except Exception as e :
            return ODSApiPdBridge.BadRequestResponse( code = 504 )

    def get2( self, apiUrl, apiEntry , apiTool, params = None ) :
        req = 0
        try :
            if type( params ) == dict :
                req = requests.get(
                            "{apiUrl}{apiEntry}/{apiVersion}/{apiTool}".format(
                                apiUrl     = apiUrl,
                                apiEntry    = apiEntry,
                                apiVersion  = self.apiVersion,
                                apiTool     = apiTool
                            ),params = params
                )
            else :
                req = requests.get(
                            "{apiUrl}{apiEntry}/{apiVersion}/{apiTool}".format(
                                apiUrl     = apiUrl,
                                apiEntry    = apiEntry,
                                apiVersion  = self.apiVersion,
                                apiTool     = apiTool
                            )
                    )
            if str( req.status_code ) == "200":
                return req
            else :
                return ODSApiPdBridge.BadRequestResponse( code = req.status_code )
        except :
            return ODSApiPdBridge.BadRequestResponse( code = 504 )

    def csvFormatToDf( self, csv, sep = ";" ) :
        return pd.read_csv( StringIO( csv.text ), sep = sep )


    def jsonFormatToDf( self, json, recordsKey = None ) :
        if type( recordsKey ) == str :
            return json_normalize( json[ recordsKey ] )
        else :
            return json_normalize( json )


    def convertToDfByFormat(    self, format = None, sep = ";",
                                recordsKey = None, data = None  ) :
        frmt = format if format != None else self.format
        if frmt == "csv" :
            return self.csvFormatToDf( csv = data, sep = sep )
        elif frmt == "json" :
            return self.jsonFormatToDf( json = data, recordsKey = recordsKey )


    def getNbDatasets( self, apiUrl ) :
        req = self.get(
            apiUrl     = apiUrl,
            apiEntry   = "datasets",
            apiTool    = "search",
            params     =   {
              "format"   : "json",
              "rows"     : "0"
            }
        )
        if type( req ) != ODSApiPdBridge.BadRequestResponse :
            return req[ "nhits" ]
        else :
            return req


    def getDatasets(    self, apiUrl = "", start = 0, rows = 10,
                        format = None, sep = ";", raw = False ) :

        frmt = format if format != None else self.format
        data = self.get(
            apiUrl     =   apiUrl,
            apiEntry   =   "datasets",
            apiTool    =   "search",
            params     =   {
                "format"  : str( frmt ),
                "rows"    : str( rows ),
                "start"   : str( start )
            }
        )
        if type( data ) == ODSApiPdBridge.BadRequestResponse :
            return data

        if raw == False :
            return json_normalize(  data = data[ "datasets" ],
                                    #record_path = ["fields"],
                                    meta = [["metas" ],["fields"]]
            )
        else :
            if frmt == "csv" :
                return data.text
            elif frmt == "json" :
                return data


    def getDatasetsInfo( self, apiUrl = "", start = 0, rows = 10 ) :
        if rows == "all" :
            nbDatasets = self.getNbDatasets( apiUrl = apiUrl )
            if type( nbDatasets ) == ODSApiPdBridge.BadRequestResponse :
                return nbDatasets
            rows = int( nbDatasets )
        data = self.getDatasets(
            apiUrl  = apiUrl,
            start   = start,
            rows    = rows )
        if type( data ) == ODSApiPdBridge.BadRequestResponse :
            return data

        df = data[ [ k for k in ODSApiPdBridge.datasetsColumns.keys() ] ]
        df.columns = ODSApiPdBridge.datasetsColumnsTitles
        shape = df.shape
        for k in ODSApiPdBridge.datasetsColumns.keys() :
            datasetsCol = ODSApiPdBridge.datasetsColumns[ k ]
            if 'cléDesDictsMembres' in datasetsCol :
                nomCol = datasetsCol[ 'enteteDeColonne' ]
                jsonProp = datasetsCol['cléDesDictsMembres' ]
                nRo = 0
                for r in range( shape[ 0 ] ) :
                    elList =  df.at[ r, nomCol ]
                    retL = []
                    for dct in elList :
                        if jsonProp in dct :
                            retL.append( dct[ jsonProp ] )
                        #str = df.at[ r, nomCol ] #row[ [ nomCol ] ]
                        #jsoned = json.loads( str )
                    df.at[ r, nomCol ] = ", ".join( retL )

        return df


    def getRecords( self, apiUrl, dataset, start = 0, rows = 10, format = None,
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
            apiUrl     =   apiUrl,
            apiEntry   =   "records",
            apiTool    =   "search",
            params     =   parametres
        )
        if type( data ) == ODSApiPdBridge.BadRequestResponse :
            return data

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
                return data
