import pandas as pd
import os
import sys
sys._enablelegacywindowsfsencoding()

class LocalCSVReader() :

    def __init__( self, dirPaths ) :
        print( dirPaths )
        if type( dirPaths ) == str :
            dirPaths = [ dirPaths ]
        self.srcDirs = dirPaths

    def listDir( self, targetDirName ) :
        return [ os.path.join( targetDirName, file ) for file in os.listdir( path = targetDirName ) ]

    def listFiles( self ) :
        ret = []
        for srcDir in self.srcDirs :
            for fileName in self.listDir( targetDirName = srcDir ) :
                ret.append( fileName  )
        return ret

    def openFile( self, filePath ) :
        print("file : " + filePath )
        print( str( os.path.exists( filePath ) ) )
        df = pd.read_csv( os.path.realpath( filePath ), sep = ";", header = 0 )
        return df

    def getFileColumns( self, filePath ) :
        return self.openFile( filePath ).columns
