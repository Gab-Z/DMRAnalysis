from threading import Thread
import requests
import sys

from lib.badRequestResponse import BadRequestResponse


class ThreadedRequest( Thread ) :


    def __init__(   self, threadId, apiUrl, apiEntry, apiTool,
                    apiVersion, params = None
    ) :
        Thread.__init__( self )
        self.threadId   = threadId
        self.apiUrl     = apiUrl
        self.apiEntry   = apiEntry
        self.apiTool    = apiTool
        self.apiVersion = apiVersion
        self.params     = params
        self.ret        = None

    def run( self ) :
        req = 0
        try :
            if type( self.params ) == dict :
                req = requests.get(
                            "{apiUrl}{apiEntry}/{apiVersion}/{apiTool}".format(
                                apiUrl      = self.apiUrl,
                                apiEntry    = self.apiEntry,
                                apiVersion  = self.apiVersion,
                                apiTool     = self.apiTool
                            ),params = self.params
                )
            else :
                req = requests.get(
                            "{apiUrl}{apiEntry}/{apiVersion}/{apiTool}".format(
                                apiUrl      = self.apiUrl,
                                apiEntry    = self.apiEntry,
                                apiVersion  = self.apiVersion,
                                apiTool     = self.apiTool
                            )
                    )
            if str( req.status_code ) == "200":
                self.ret = req
            else :
                self.ret = BadRequestResponse( code = req.status_code )
        except OSError :
            print( "I/O error({0}): {1}".format(OSError.errno, OSError.strerror) )
        except ValueError:
            print( ValueError )
        except requests.exceptions.RequestException as e :
            print( e )
        except :
            self.ret = BadRequestResponse( code = 504 )
