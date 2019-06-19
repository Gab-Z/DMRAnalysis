from lib.ODSApiPdBridge import ODSApiPdBridge
from lib.LocalCSVReader import LocalCSVReader
from tkinter import *
import tkinter.ttk as ttk
import os
import datetime
import dateutil.parser as dateParser
from lib.misc import wrapped_partial

class ODSApiPdBridgeGUI( ODSApiPdBridge, LocalCSVReader, Tk ) :

    styles = {
        "couleurs" : {
            "defaultBg"     : "#e0e0e0",
            "darkBg"        : "#606060",
            "brightBg"      : "#e0cf9a",
            "defaultFont"   : "#343434"
        },
        "polices" : {
            "default"       : "Courier 12"
        }
    }
    datasetKeyForLocalFiles = "- -"


    def __init__( self, apiUrls = None, apiVersion = "1.0", responseFormat = "json", localDirs = [] ) :

        ODSApiPdBridge.__init__(
            self, apiUrls = apiUrls, apiVersion = apiVersion,
            responseFormat = responseFormat
        )
        LocalCSVReader.__init__( self, dirPaths = localDirs )
        Tk.__init__( self )

        self.title( "OpenData Bridge" )
        self.minsize(  900, 400 )
        self.noteBook = ttk.Notebook( self )

        self.views = {}
        self.addView( name = "accueil", tabText = "Jeux de données", bg = self.coul( "darkBg" ) )
        self.addView( name = "dataset", tabText = "Graphiques", bg = self.coul( "darkBg" ) )
        self.browserTrees = self.addBrowseView( parent = self.views[ "accueil" ] )
        self.noteBook.pack( expand = YES, fill = BOTH  )
        #self.after( 10, self.addDatasetsToTreeview )
        #self.bind( "<Visibility>", self.startupEvent )
        self.after_idle( self.startupEvent )
        self.mainloop()

    def pol( self, _police ) :
        return ODSApiPdBridgeGUI.styles[ "polices" ][ _police ]
    def coul( self, _couleur ) :
        return ODSApiPdBridgeGUI.styles[ "couleurs" ][ _couleur ]

    def startupEvent( self ) :
        #self.unbind( "<Visibility>" )
        self.after( 100, self.addDatasetsToTreeview )

    def addView( self, name = None, tabText = "", width = 100, height = 100, bg = None, borderwidth = 0, highlightthickness = 0 ) :
        self.views[ str( name ) ] = Frame( self,  width = 100, height = 100, bg = bg if bg != None else self.coul( "defaultBg" ), borderwidth = borderwidth, highlightthickness = highlightthickness )
        self.noteBook.add( self.views[ str( name ) ], text = '\n {} '.format( tabText ) )

        return self.views[ str( name ) ]

    def openView( self, viewName ) :
        for view in self.views.values() :
            view.forget()
        self.views[ viewName ].pack( expand = YES, fill = BOTH )

    def adjustFormat( self, data ) :
        try :
            date = dateParser.parse( data ) #, '%Y-%m-%d%Z:%H:%M+%H:%M'
            return date.strftime( '%d/%m/%Y' )
        except :
            return data

    def addBrowseView( self, parent ) :

        menuFrame = Frame( parent, height = 50, bg = self.coul( "defaultBg" ), borderwidth = 0, highlightthickness = 0 )
        menuFrame.pack( expand = NO, fill = X )
        txtCont = Frame( menuFrame, height = 50, bg = self.coul( "defaultBg" ), borderwidth = 0, highlightthickness = 0 )
        txtCont.grid( column = 0, row = 0, columnspan = 2, sticky = "ew" )
        txtArea = Text( txtCont, state = DISABLED, height = 2 )

        menuBtCont = Frame( menuFrame, height = 50, bg = self.coul( "defaultBg" ), borderwidth = 0, highlightthickness = 0 )
        #menuBtCont.place( relx = 0.5, rely = 0.5, anchor = "w" )
        menuBtCont.grid( column = 2, row = 0, sticky = "ew"  )
        txtArea.pack( anchor = "ne", fill = X )
        validButton = Button( menuBtCont, text = "Ouvrir un jeu de données", command = self.selectDataset )
        validButton.grid( column = 0, row = 0, sticky = "ew" )

        remoteFrame = Frame( parent,  width = 100, height = 100, bg = self.coul( "defaultBg" ), borderwidth = 0, highlightthickness = 0 )
        remoteFrame.pack( expand = YES, fill = BOTH, anchor = "ne", side = TOP )
        remoteTree = self.addTreeview( parent = remoteFrame )
        return {
            'frame'    : remoteFrame,
            'tree'     : remoteTree,
            'textArea' : txtArea
        }

    def addTreeview( self, parent ) :
        tree = ttk.Treeview ( parent )
        tree[ 'selectmode' ] = 'browse'
        datasetColTitles = self.getDatasetsColumnsTitle().copy() # [ 'nomCol1, 'nomCol2', 'nomCol3',... ]
        colsTitlesAndNum = [ colKey + "_" + str( idx ) for idx, colKey in enumerate( datasetColTitles ) ] # [ 'nomCol1_0',' 'nomCol2_1', 'nomCol3_2',...]
        tree[ "columns" ] = colsTitlesAndNum[ 1:: ] # [ 'nomCol2_1', 'nomCol3_2',...]
        colsTitlesAndNum[ 0 ] = "#0" # [ '#0', 'nomCol2_1', 'nomCol3_2',...]
        for idx, colName in enumerate( colsTitlesAndNum ) :
            tree.column( colName, stretch = YES )
            tree.heading( colName, text = datasetColTitles[ idx ], anchor = W )

        vsb = ttk.Scrollbar( parent, orient = "vertical", command = tree.yview )
        vsb.pack( side = 'right', fill = 'y' )
        tree.configure( yscrollcommand = vsb.set )
        tree.pack( expand = YES, fill = BOTH )

        #self.addDatasetsToTreeview( tree )
        return tree

    def addDatasetsToTreeview( self, tree = False, sortAscending = True  ) :
        tree = tree if tree else self.browserTrees[ 'tree' ]
        datasetColTitles = self.getDatasetsColumnsTitle().copy()
        idxCount = 0
        for urlIdx, url in enumerate( self.apiUrls ) :
            dfDatasets = self.getDatasetsInfo( apiUrl = url, rows = "all" )
            if type( dfDatasets ) != ODSApiPdBridge.BadRequestResponse :
                folderRow = tree.insert( "", urlIdx, text = url )
                orderedDf = dfDatasets.sort_values( by = self.getColumnSortingPriority()[ 0 ], kind = 'mergesort', ascending = sortAscending ).reset_index( drop = True )
                for idx, row in orderedDf.iterrows() :
                    tree.insert( folderRow, idx + 1,
                        text = self.adjustFormat( row[ datasetColTitles[ 0 ] ] ),
                        values = [ self.adjustFormat( row[ colTitle ] ) for colTitle in datasetColTitles[ 1 :: ] ]
                    )
            else :
                folderRow = tree.insert( "", urlIdx, text = 'Echec de la connexion à {url} : erreur {numErreue}'.format( url = url, numErreue = str( dfDatasets.code ) ) )
            idxCount = urlIdx

        self.addLocalFilesToTreeview( tree, idxCount + 1  )

    def addLocalFilesToTreeview( self, tree, startIdx ) :
        folderRow = tree.insert( "", startIdx, text = 'Fichiers locaux' )
        filesList = self.listFiles()
        for idx, f in enumerate( filesList ) :
            df = self.openFile( f )
            cols = df.columns
            rows = df.shape[ 0 ]
            if len( cols ) >= 3 :
                tree.insert( folderRow, idx, text = os.path.split( f )[ 1 ], values = ( rows, ODSApiPdBridgeGUI.datasetKeyForLocalFiles, ODSApiPdBridgeGUI.datasetKeyForLocalFiles, ", ".join( cols ) ) )

    def clearTreeview( self, tree ) :
        children = tree.get_children()
        for item in children :
            tree.delete( item )

    def selectDataset( self ) :
        textArea = self.browserTrees[ 'textArea' ]
        self.clearLog( textArea = textArea )
        tree = self.browserTrees[ 'tree' ]
        curItem = tree.item( tree.focus() )
        if len( tree.selection() ) != 1 or len( curItem[ 'values'] ) == 0 :
            self.writeLog( textArea, "Veuillez sélectionner un dataset dans la liste" )
            self.after( 3000, wrapped_partial( self.clearLog, textArea = textArea ) )
            return False
        print( curItem )
        datasetIdPos = self.getDatasetsColumnsTitle().index( 'datasetid' )
        datasetId = None
        isLocalFile = False
        if datasetIdPos == 0 :
            datasetId = curItem[ 'text' ]
        else :
            datasetId = curItem[ 'values' ][ datasetIdPos - 1 ]
        if datasetId == ODSApiPdBridgeGUI.datasetKeyForLocalFiles :
            datasetId = curItem[ 'text' ]
            isLocalFile = True
        self.openDataset( datasetId = datasetId, isLocalFile = isLocalFile, columns = curItem[ 'values' ][ self.getDatasetsColumnsTitle().index( 'Colonnes' ) - 1 ]  )

    def writeLog( self, textArea, txt ) :
        textArea.config( state = NORMAL )
        textArea.delete( 1.0, END )
        textArea.insert( END, txt )
        textArea.config( state = DISABLED )

    def clearLog( self, textArea ) :
        textArea.config( state = NORMAL )
        textArea.delete( 1.0, END )
        textArea.config( state = DISABLED )

    def openDataset( self, datasetId, isLocalFile, columns ) :
        columns = columns.split( ", " )
        print( datasetId + ' ' + str( isLocalFile )+ ' ' + str( columns ) + ' ' + str( type( columns ) ) )
        return False
