from lib.ODSApiPdBridge import ODSApiPdBridge
from lib.LocalCSVReader import LocalCSVReader
from tkinter import *
import tkinter.ttk as ttk
import os
import datetime
import dateutil.parser as dateParser
from functools import partial

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


    def __init__( self, apiUrls = None, apiVersion = "1.0", responseFormat = "json", localDirs = [] ) :

        ODSApiPdBridge.__init__(
            self, apiUrls = apiUrls, apiVersion = apiVersion,
            responseFormat = responseFormat
        )
        LocalCSVReader.__init__( self, dirPaths = localDirs )
        Tk.__init__( self )

        self.title( "OpenData Bridge" )
        self.minsize(  900, 400 )
        '''
        self.menu = Frame( self, height = 50, bg = self.coul( "defaultBg" ), borderwidth = 0, highlightthickness = 0 )
        self.menu.pack( expand=0, fill=X )
        self.menuBtCont = Frame( self.menu, height = 50, bg = self.coul( "defaultBg" ), borderwidth = 0, highlightthickness = 0 )
        self.menuBtCont.place( relx = 0.5, rely = 0.5, anchor = "c" )
        for i in range( 10 ) :
            b = Button( self.menuBtCont, text = "BT_" + str( i ) )
            b.grid( column = i, row = 0, padx = 10, sticky = "e")
        '''
        self.views = {}
        self.addView( name = "accueil", bg = self.coul( "darkBg" ) )
        self.browserTrees = self.addBrowseView( parent = self.views[ "accueil" ] )

        self.openView( "accueil" )

    def pol( self, _police ) :
        return ODSApiPdBridgeGUI.styles[ "polices" ][ _police ]
    def coul( self, _couleur ) :
        return ODSApiPdBridgeGUI.styles[ "couleurs" ][ _couleur ]

    def addView( self, name = None, width = 100, height = 100, bg = None, borderwidth = 0, highlightthickness = 0 ) :
        self.views[ str( name ) ] = Frame( self,  width = 100, height = 100, bg = bg if bg != None else self.coul( "defaultBg" ), borderwidth = borderwidth, highlightthickness = highlightthickness )
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
        txtCont.grid( column = 0, row = 0, columnspan = 6 )
        txtArea = Text( txtCont, state = DISABLED, height = 2 )
        txtArea.pack( anchor = "ne", fill = X )
        menuBtCont = Frame( menuFrame, height = 50, bg = self.coul( "defaultBg" ), borderwidth = 0, highlightthickness = 0 )
        #menuBtCont.place( relx = 0.5, rely = 0.5, anchor = "w" )
        menuBtCont.grid( column = 6, row = 0  )
        validButton = Button( menuBtCont, text = "Ouvrir un jeu de données", command = self.openDataset )
        validButton.grid( column = 0, row = 0, padx = 10, sticky = "e")

        remoteFrame = Frame( parent,  width = 100, height = 100, bg = self.coul( "defaultBg" ), borderwidth = 0, highlightthickness = 0 )
        remoteFrame.pack( expand = YES, fill = BOTH, anchor = "ne", side = TOP )
        remoteTree = self.addRemoteTreeview( parent = remoteFrame )
        return {
            'frame'    : remoteFrame,
            'tree'     : remoteTree,
            'textArea' : txtArea
        }

    def addRemoteTreeview( self, parent ) :
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

        self.addDatasetsToTreeview( tree )

        return tree

    def remoteTreeSelect( self, event ) :
        print("sel remote")
        localTree = self.browserTrees[ 'localFrame' ][ 'tree' ]
        remoteTree = self.browserTrees[ 'remoteFrame' ][ 'tree' ]
        localTree.bind( '<<TreeviewSelect>>', lambda a : False )
        remoteTree.bind( '<<TreeviewSelect>>', lambda a : False )

        if len( localTree.selection() ) > 0 :
            for itemSelected in localTree.selection() :
                localTree.selection_remove( itemSelected )
        #localTree.bind( '<<TreeviewSelect>>', self.localTreeSelect )

        selItem = remoteTree.focus()

        remoteTree.selection_set( selItem )
        #remoteTree.focus_set()
        #remoteTree.focus( selItem )
        remoteTree.bind( '<<TreeviewSelect>>', self.remoteTreeSelect )
        localTree.bind( '<<TreeviewSelect>>', self.localTreeSelect )

    def localTreeSelect( self, event ) :
        print( "sel local" )
        remoteTree = self.browserTrees[ 'remoteFrame' ][ 'tree' ]
        localTree = self.browserTrees[ 'localFrame' ][ 'tree' ]
        remoteTree.bind( '<<TreeviewSelect>>', lambda a : False )
        localTree.bind( '<<TreeviewSelect>>', lambda a : False )
        if len( remoteTree.selection() ) > 0 :
            for itemSelected in remoteTree.selection() :
                remoteTree.selection_remove( itemSelected )

        selItem = localTree.focus()

        localTree.selection_set( selItem )
        #localTree.focus_set()
        #localTree.focus( selItem )
        localTree.bind( '<<TreeviewSelect>>', self.localTreeSelect )
        remoteTree.bind( '<<TreeviewSelect>>', self.remoteTreeSelect )

    def addDatasetsToTreeview( self, tree, sortAscending = True  ) :
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
                tree.insert( folderRow, idx, text = os.path.split( f )[ 1 ], values = ( rows, "- -", "- -", ", ".join( cols ) ) )

    def clearTreeview( self, tree ) :
        children = tree.get_children()
        for item in children :
            tree.delete( item )

    def addLocalTreeviewOLD( self, parent ) :

        tree =  ttk.Treeview ( parent )
        tree[ 'selectmode' ] = 'browse'
        tree["columns"]=( "one", "two" )
        tree.column( "#0", stretch = YES )
        tree.heading( "#0", text = "Fichiers locaux", anchor = W )
        tree.column( "one", stretch = YES )
        tree.heading( "one", text = "Enregistrements", anchor = W )
        tree.column( "two", stretch = YES )
        tree.heading( "two", text = "Colonnes", anchor = W )


        vsb = ttk.Scrollbar( parent, orient = "vertical", command = tree.yview )
        vsb.pack( side = 'right', fill = 'y' )
        tree.configure( yscrollcommand = vsb.set )
        tree.bind( '<<TreeviewSelect>>', self.localTreeSelect )
        tree.pack( expand = YES, fill = BOTH )
        filesList = self.listFiles()
        for idx, f in enumerate( filesList ) :
            df = self.openFile( f )
            cols = df.columns
            rows = df.shape[ 0 ]
            if len( cols ) >= 3 :
                tree.insert( "", idx + 1, text = os.path.split( f )[ 1 ], values = ( rows, ", ".join( cols ) ) )
        return tree

    def openDataset( self ) :
        tree = self.browserTrees[ 'tree' ]
        if len( tree.selection() ) != 1 :
            textArea = self.browserTrees[ 'textArea' ]
            self.writeLog( textArea, "Veuillez sélectionner un dataset dans la liste" )
            self.after( 3, partial( lambda a : self.clearLog, textArea = textArea ) )

    def writeLog( self, textArea, txt ) :
        textArea.config( state = NORMAL )
        textArea.delete( 1.0, END )
        textArea.insert( END, txt )
        textArea.config( state = DISABLED )

    def clearLog( self, textArea ) :
        textArea.config( state = NORMAL )
        textArea.delete( 1.0, END )
        textArea.config( state = DISABLED )
