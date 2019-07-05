import pandas as pd
import os
import platform
import sys
if platform.system() == "Windows" :
    sys._enablelegacywindowsfsencoding()

class LocalCSVReader() :

    def __init__( self, dirPaths ) :
        if type( dirPaths ) == str :
            dirPaths = [ dirPaths ]
        self.srcDirs = dirPaths

        self.loadedDataFrames = {}

    def listDir( self, targetDirName ) :
        return [ os.path.join( targetDirName, file ) for file in os.listdir( path = targetDirName ) ]

    def listFiles( self ) :
        ret = []
        for srcDir in self.srcDirs :
            for fileName in self.listDir( targetDirName = srcDir ) :
                ret.append( fileName  )
        return ret

    def openFile( self, filePath ) :

        df = pd.read_csv( os.path.realpath( filePath ), sep = ";", header = 0 )
        return df

    def getStaticDataFrame( self, fileName ) :
        if fileName not in self.loadedDataFrames :
            filePath = os.path.join( self.srcDirs[ 0 ], fileName )
            self.loadedDataFrames[ 'fileName' ] = self.openFile( filePath )
        return self.loadedDataFrames[ 'fileName' ]
