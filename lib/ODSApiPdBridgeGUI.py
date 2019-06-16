from lib.ODSApiPdBridge import ODSApiPdBridge
from lib.LocalCSVReader import LocalCSVReader
from tkinter import *
import os


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


    def __init__( self, apiUrl = None, apiVersion = "1.0", responseFormat = "json", localDirs = [] ) :

        ODSApiPdBridge.__init__(
            self, apiUrl = apiUrl, apiVersion = apiVersion,
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
        print( len( filesList ) )
        self.filesListBox = Listbox ( self.views[ "accueil" ] )
        for idx, filePath in enumerate( filesList ) :
            print( os.path.split( filePath )[ 1 ] )
            self.filesListBox.insert( idx, os.path.split( filePath )[ 1 ] )
        self.filesListBox.pack()
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
