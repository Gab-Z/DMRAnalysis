from lib.ODSApiPdBridge import ODSApiPdBridge
from lib.LocalCSVReader import LocalCSVReader
import tkinter as tk
import tkinter.ttk as ttk
import os
import datetime
import dateutil.parser as dateParser
from lib.misc import wrapped_partial
from lib.PdSrToGraph import PdSrToGraph
from lib.AnalysisGMPlot import afficherDispersionAnomalies

class ODSApiPdBridgeGUI( ODSApiPdBridge, LocalCSVReader, tk.Tk ) :

    styles = {
        "couleurs" : {
            "defaultBg"     : "#e0e0e0",
            "darkBg"        : "#606060",
            "brightBg"      : "#e0cf9a",
            "defaultFont"   : "#343434",
            "loadCol"       : "#e6761a"
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
        tk.Tk.__init__( self )

        self.title( "OpenData Bridge" )
        self.minsize(  900, 400 )
        self.noteBook = ttk.Notebook( self )

        self.views = {}
        self.addView( name = "menu", tabText = "Menu", bg = self.coul( "darkBg" ) )
        self.addView( name = "accueil", tabText = "Jeux de données", bg = self.coul( "darkBg" ) )
        #self.addView( name = "dataset", tabText = "Graphiques", bg = self.coul( "darkBg" ) )
        self.browserTrees = self.addBrowseView( parent = self.views[ "accueil" ] )
        self.noteBook.pack( expand = 'yes', fill = 'both'  )
        #self.after( 10, self.addDatasetsToTreeview )
        #self.bind( "<Visibility>", self.startupEvent )
        self.createMenu( self.views[ 'menu' ] )
        self.addDatasetsToTreeview()
        self.mainloop()

    def pol( self, _police ) :
        return ODSApiPdBridgeGUI.styles[ "polices" ][ _police ]
    def coul( self, _couleur ) :
        return ODSApiPdBridgeGUI.styles[ "couleurs" ][ _couleur ]


    def addView( self, name = None, tabText = "", width = 100, height = 100, bg = None, borderwidth = 0, highlightthickness = 0 ) :
        self.views[ str( name ) ] = tk.Frame( self,  width = 100, height = 100, bg = bg if bg != None else self.coul( "defaultBg" ), borderwidth = borderwidth, highlightthickness = highlightthickness )

        self.noteBook.add(
            self.views[ str( name ) ],
            text = '\n {} '.format( tabText )
        )

        return self.views[ str( name ) ]

    def openView( self, viewName ) :
        for view in self.views.values() :
            view.forget()
        self.views[ viewName ].pack( expand = 'yes', fill = 'both' )

    def adjustFormat( self, data ) :
        try :
            date = dateParser.parse( data ) #, '%Y-%m-%d%Z:%H:%M+%H:%M'
            return date.strftime( '%d/%m/%Y' )
        except :
            return data

    def createMenu( self, parent ) :
        cont = tk.Frame( parent, bg = self.coul( "defaultBg" ) )
        cont.pack( expand = 'yes', fill = 'both' )
        cont.grid_propagate( True )
        cont.columnconfigure( 0, weight = 1 )
        #cont.columnconfigure( 1, weight = 1 )
        cont.columnconfigure( 2, weight = 1 )
        headColSep = ttk.Separator( cont, orient = "vertical" )
        headColSep.grid( column = 1, row = 1, sticky = "n" )

        bodyColSep = ttk.Separator( cont, orient = "vertical" )
        bodyColSep.grid( column = 1, row = 3, rowspan = 3, sticky = "n" )

        titleLabel = tk.Label( cont, text = "Menu")
        titleLabel.grid( column = 0, row = 0, columnspan = 3, sticky = "ew" )
        staticFuncLabel = tk.Label( cont, text = "Paris.fr - Dans ma rue")
        staticFuncLabel.grid( column = 0, row = 2, sticky = "ew" )
        dynamicFuncLabel = tk.Label( cont, text = "Autres jeux de données")
        dynamicFuncLabel.grid( column = 2, row = 2, sticky = "ew" )

        cont.rowconfigure( 3, minsize = 5, pad = 5 )
        sep = ttk.Separator( cont, orient = "horizontal" )
        sep.grid( column = 0, row = 3, columnspan = 3, sticky="ew" )

        but_anomArrAnnees = tk.Button( cont, text = "Anomalies signalées par arrondissement et par année")
        but_anomArrAnnees.grid( column = 0, row = 4, sticky = "ew" )

        but_anomTypeMois = tk.Button( cont, text = "Anomalies signalées par type et par mois" )
        but_anomTypeMois.grid( column = 0, row = 5, sticky = "ew" )

        but_anomTypeArr = tk.Button( cont, text = "Anomalies signalées par arrondissement et par type" )
        but_anomTypeArr.grid( column = 0, row = 6, sticky = "ew" )

        but_anomArrAnnees.bind( '<Button-1>', self.openAnomParArrAnn )
        but_anomTypeMois.bind( '<Button-1>', self.openAnomTypeMois )
        but_anomTypeArr.bind( '<Button-1>', self.openAnomTypeArr )

        but_cartographie = tk.Button( cont, text = "Cartographie GoogleMaps" )
        but_cartographie.grid( column = 0, row = 7, sticky = "ew" )
        but_cartographie.bind( '<Button-1>', self.openCartoGoogle )


    def openAnomParArrAnn( self, event ) :
        df = self.getStaticDataFrame( 'dans-ma-rue.csv' )
        self.openGraph(
            viewName = "Anomalies par arrondissement et par année",
            pandasSerie = df.groupby( [ 'ANNEE DECLARATION', 'ARRONDISSEMENT' ] ).size()
        )
    def openAnomTypeMois( self, event ) :
        df = self.getStaticDataFrame( 'dans-ma-rue.csv' )
        self.openGraph(
            viewName = "Anomalies par type et par mois",
            pandasSerie = df.groupby( [ 'MOIS DECLARATION', 'SOUSTYPE' ] ).size(),
            startDrawFunc = 'automerged'
        )

    def openAnomTypeArr( self, event) :
        df = self.getStaticDataFrame( 'dans-ma-rue.csv' )
        self.openGraph(
            viewName = "Anomalies par arrondissement et par type",
            pandasSerie = df.groupby( [ 'ARRONDISSEMENT', 'TYPE'] ).size(),
            startDrawFunc = 'automerged'
        )

    def openGraph( self, viewName, pandasSerie, startDrawFunc = None ) :
        if viewName not in self.views :
            self.addView( name = viewName, tabText = viewName, bg = self.coul( "darkBg" ) )
        self.views[ viewName ].graph = PdSrToGraph(
            parent = self.views[ viewName ],
            serie = pandasSerie,
            startDrawFunc = startDrawFunc
        )
        self.noteBook.select( self.views[ viewName ] )

    def openCartoGoogle( self, event ) :
        df = self.getStaticDataFrame( 'dans-ma-rue.csv' )
        afficherDispersionAnomalies( df )

    def addBrowseView( self, parent ) :

        menuFrame = tk.Frame( parent, height = 50, bg = self.coul( "defaultBg" ), borderwidth = 0, highlightthickness = 0 )
        menuFrame.pack( expand = 'no', fill = 'x' )
        txtCont = tk.Frame( menuFrame, height = 50, bg = self.coul( "defaultBg" ), borderwidth = 0, highlightthickness = 0 )
        txtCont.grid( column = 0, row = 0, columnspan = 2, sticky = "ew" )
        txtArea = tk.Text( txtCont, state = 'disabled', height = 2 )

        menuBtCont = tk.Frame( menuFrame, height = 50, bg = self.coul( "defaultBg" ), borderwidth = 0, highlightthickness = 0 )
        #menuBtCont.place( relx = 0.5, rely = 0.5, anchor = "w" )
        menuBtCont.grid( column = 2, row = 0, sticky = "ew"  )
        txtArea.pack( anchor = "ne", fill = 'x' )
        validButton = tk.Button( menuBtCont, text = "Ouvrir un jeu de données", command = self.selectDataset )
        validButton.grid( column = 0, row = 0, sticky = "ew" )

        remoteFrame = tk.Frame( parent,  width = 100, height = 100, bg = self.coul( "defaultBg" ), borderwidth = 0, highlightthickness = 0 )
        remoteFrame.pack( expand = 'yes', fill = 'both', anchor = "ne", side = 'top' )

        #loaderCont = Frame( parent, height = 30, bg = self.coul( "defaultBg" ), borderwidth = 0, highlightthickness = 0 )
        #self.filesProgressBar = ttk.Progressbar( loaderCont, mode = 'determinate', maximum = 100, length = 300 )
        #self.filesProgressBar = Canvas( loaderCont, width = 300, height = 30, bg = self.coul( "defaultBg" ), borderwidth = 0, highlightthickness = 0 )
        #self.filesProgressBar.loadValue = 0
        #self.filesProgressBar.loadMax = 100
        #loaderCont.pack( fill = X, anchor = "ne", side = TOP )
        #loaderCont.pack_propagate( 0 )
        #self.filesProgressBar.place( relx = 0.5, rely = 0.5, anchor = "c" )

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
            tree.column( colName, stretch = 'yes' )
            tree.heading( colName, text = datasetColTitles[ idx ], anchor = 'w' )

        vsb = ttk.Scrollbar( parent, orient = "vertical", command = tree.yview )
        vsb.pack( side = 'right', fill = 'y' )
        tree.configure( yscrollcommand = vsb.set )
        tree.pack( expand = 'yes', fill = 'both' )

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


        apiUrl =  tree.item( tree.parent( tree.focus() ) )[ 'text' ]

        enregistrementsPos = datasetIdPos = self.getDatasetsColumnsTitle().index( 'Enregistrements' )
        nbEnregistrements = 0
        if enregistrementsPos == 0 :
            nbEnregistrements = curItem[ 'text' ]
        else :
            nbEnregistrements = curItem[ 'values' ][ enregistrementsPos - 1 ]


        self.openDataset(
            datasetId = datasetId, isLocalFile = isLocalFile,
            columns = curItem[ 'values' ][ self.getDatasetsColumnsTitle().index( 'Colonnes' ) - 1 ],
            nbEnregistrements = nbEnregistrements,
            apiUrl = apiUrl
        )

    def writeLog( self, textArea, txt ) :
        textArea.config( state = 'normal' )
        textArea.delete( 1.0, 'end' )
        textArea.insert( 'end', txt )
        textArea.config( state = 'disabled' )

    def clearLog( self, textArea ) :
        textArea.config( state = 'normal' )
        textArea.delete( 1.0, 'end' )
        textArea.config( state = 'disabled' )


    def openDataset( self, datasetId, isLocalFile, columns, nbEnregistrements, apiUrl ) :
        columns = columns.split( ", " )
        jsn = self.getRecords( apiUrl, datasetId, start = 0, rows = nbEnregistrements )
        return False
