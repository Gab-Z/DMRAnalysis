from lib.ODSApiPdBridge import ODSApiPdBridge
from lib.LocalCSVReader import LocalCSVReader
from tkinter import *
import tkinter.ttk as ttk
import os
import datetime
import dateutil.parser as dateParser

class ODSApiPdBridgeGUI( ODSApiPdBridge, LocalCSVReader, Tk ) :

    styles = {
        "couleurs" : {
            "defaultBg"     : "#e0e0e0",
            "darkBg"        : "#606060",
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
        self.menu = Frame( self, height = 50, bg = self.coul( "defaultBg" ), borderwidth = 0, highlightthickness = 0 )
        self.menu.pack( expand=0, fill=X )
        self.menuBtCont = Frame( self.menu, height = 50, bg = self.coul( "defaultBg" ), borderwidth = 0, highlightthickness = 0 )
        self.menuBtCont.place( relx = 0.5, rely = 0.5, anchor = "c" )

        for i in range( 10 ) :
            b = Button( self.menuBtCont, text = "BT_" + str( i ) )
            #b.pack( side = LEFT, anchor = CENTER, padx = 10)
            b.grid( column = i, row = 0, padx = 10, sticky = "e")

        self.views = {}
        self.addView( name = "accueil", bg = self.coul( "darkBg" ) )
        filesList = self.listFiles()

        self.datasetsTree = ttk.Treeview ( self.views[ "accueil" ] )


        #self.datasetsTree[ "columns" ]=( "one", "two", "three" )
        datasetColTitles = self.getDatasetsColumnsTitle().copy() # [ 'nomCol1, 'nomCol2', 'nomCol3',... ]
        colsTitlesAndNum = [ colKey + "_" + str( idx ) for idx, colKey in enumerate( datasetColTitles ) ] # [ 'nomCol1_0',' 'nomCol2_1', 'nomCol3_2',...]
        self.datasetsTree[ "columns" ] = colsTitlesAndNum[ 1:: ] # [ 'nomCol2_1', 'nomCol3_2',...]
        colsTitlesAndNum[ 0 ] = "#0" # [ '#0', 'nomCol2_1', 'nomCol3_2',...]
        for idx, colName in enumerate( colsTitlesAndNum ) :
            self.datasetsTree.column( colName, stretch = YES )
            self.datasetsTree.heading( colName, text = datasetColTitles[ idx ], anchor = W )


        vsb = ttk.Scrollbar( self.views[ "accueil" ], orient = "vertical", command = self.datasetsTree.yview )
        vsb.pack( side = 'right', fill = 'y' )
        self.datasetsTree.configure( yscrollcommand = vsb.set )

        dfDatasets = self.getDatasetsInfo( rows = "all" )
        if type( dfDatasets ) != ODSApiPdBridge.BadRequestResponse :
            dfDatasets.sort_values( by = self.getColumnSortingPriority(), kind = 'mergesort', inplace = True )
            for idx, row in dfDatasets.iterrows() :
                #self.datasetsTree.insert( "", idx + 1, values = ( row[ "datasetid" ], row[ "Enregistrements" ] ) )
                self.datasetsTree.insert( "", idx + 1,
                    text = self.adjustFormat( row[ datasetColTitles[ 0 ] ] ),
                    values = [ self.adjustFormat( row[ colTitle ] ) for colTitle in datasetColTitles[ 1 :: ] ]
                )



        self.fichiersTree =  ttk.Treeview ( self.views[ "accueil" ] )
        self.fichiersTree["columns"]=( "one", "two" )
        self.fichiersTree.column( "#0", width = 100, minwidth = 100, stretch = YES )
        self.fichiersTree.heading( "#0", text = "Nom de fichier", anchor = W )
        self.fichiersTree.column( "one", width = 100, minwidth = 100, stretch = YES )
        self.fichiersTree.heading( "one", text = "Nb Enregistrements", anchor = W )
        self.fichiersTree.column( "two", width = 350, minwidth = 250, stretch = YES )
        self.fichiersTree.heading( "two", text = "Colonnes", anchor = W )


        #self.brancheLocale = self.datasetsTree.insert( "", 1, text = "Fichiers locaux" )
        #self.brancheDistante = self.datasetsTree.insert( "", 1, text = "Jeux de données distants" )
        for idx, f in enumerate( filesList ) :
            cols = self.getFileColumns( f )
            if len( cols ) >= 3 :
                self.fichiersTree.insert( "", idx + 1, text =  os.path.split( f )[ 1 ], values = ( 0, ", ".join( cols) ) )



        #tree.insert("" , 0,    text="Line 1", values=("1A","1b"))
        '''
        for idx, filePath in enumerate( filesList ) :
            print( os.path.split( filePath )[ 1 ] )
            self.filesListBox.insert( idx, os.path.split( filePath )[ 1 ] )
        '''
        self.datasetsTree.pack( expand=YES, fill=BOTH )
        self.fichiersTree.pack( expand=YES, fill=BOTH )
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
        #self.views[ viewName ].grid( row = 0, column = 0, padx = 0, pady = 0, sticky = "nw" )
        self.views[ viewName ].pack( expand=YES, fill=BOTH )
        #self.views[ viewName ].scale("all",0,0,wscale,hscale)

    def adjustFormat( self, data ) :
        try :
            date = dateParser.parse( data ) #, '%Y-%m-%d%Z:%H:%M+%H:%M'
            return date.strftime( '%d/%m/%Y' )
        except :
            return data

    def addRemoteTreeview( self, parent ) :
        tree = ttk.Treeview ( parent )
        #self.datasetsTree[ "columns" ]=( "one", "two", "three" )
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

        for urlIdx, url in enumerate( self.apiUrls ) :
            dfDatasets = self.getDatasetsInfo( apiUrl = url, rows = "all" )
            folderRow = tree.insert( "", urlIdx, text = url )
            if type( dfDatasets ) != ODSApiPdBridge.BadRequestResponse :
                dfDatasets.sort_values( by = self.getColumnSortingPriority(), kind = 'mergesort', inplace = True )
                for idx, row in dfDatasets.iterrows() :
                    #self.datasetsTree.insert( "", idx + 1, values = ( row[ "datasetid" ], row[ "Enregistrements" ] ) )
                    tree.insert( folderRow, idx + 1,
                        text = self.adjustFormat( row[ datasetColTitles[ 0 ] ] ),
                        values = [ self.adjustFormat( row[ colTitle ] ) for colTitle in datasetColTitles[ 1 :: ] ]
                    )
