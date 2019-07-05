import pandas as pd
import os
import platform
from pathlib import Path

from tkinter import *
import math
from pprint import pprint
import random
import colorsys
from tkinter import font



from tkinter import font
import tkinter.ttk as ttk

from lib.misc import wrapped_partial
import lib.customTkComponents as customTk


class PdSrToGraph() :


    def __init__(
        # instance de classe
        self,
        # tkWidget auquel attacher le canvas
        parent,
        # serie Pandas à traiter
        serie,
        startDrawFunc = None,
        # marge horizontale entre groupes de colonnes relative à
        # largeur de colonne
        marginGroupRatio    = 0.5,
        maxMarginGroup      = 100,
        # marge horizontale entre colonnes relative à la largeur des
        # colonnes
        marginColRatio      = 0,
        # marge horizontale entre les labels et les bords des colonnes
        # relative à la largeur des labels
        paddingColRatio     = 0.4,
        maxPaddingCol       = 5,
        # marge verticale autour des labels relative à la hauteur des
        # labels
        marginLabelRatio    = 0.2,
        # marge horizontale à autour des noms de labels. Relatif à la
        # largeur des noms
        marginNamesRatio   = 0.2,
        # largeur maximale d'une colonne en pixels
        maxColBlockWidth    = 50,
        # largeur maximale des titres d'axes en pixels
        maxNamesWidth       = 200,
        # police des titres des axes
        nameFont            = "Verdana",
        nameSize          = 14,
        # police des labels de pied de colonne
        labelFont           = "Verdana",
        labelSize           = 14,
        # police des valeurs en haut de colonne
        valueFont           = "Verdana",
        valueSize          = 10,
        groupHeight         = 600
    ) :

        self.parent              = parent
        self.marginGroupRatio    = marginGroupRatio
        self.maxMarginGroup      = maxMarginGroup
        self.marginColRatio      = marginColRatio
        self.paddingColRatio     = paddingColRatio
        self.maxPaddingCol       = maxPaddingCol
        self.marginLabelRatio    = marginLabelRatio
        self.marginNamesRatio    = marginNamesRatio
        self.maxColBlockWidth    = maxColBlockWidth
        self.maxNamesWidth       = maxNamesWidth

        self.serie               = serie
        self.canvasBackground    = '#d1d1d1',
        self.groupHeight         = groupHeight

        self.groupHeightVar = IntVar()
        self.groupHeightVar.set( self.groupHeight )

        self.system = platform.system()
        self.maxToolPanelWidth = 600

        self.curGroupFunc = self.drawSplitedGroups,
        self.curPrintFunc = self.printHist,
        self.curNbGroupsPerCol = 1,
        self.curNestLevel = 0

        self.nameFontVar = StringVar()
        self.nameFontVar.set( nameFont )
        self.nameFontSize = IntVar()
        self.nameFontSize.set( nameSize )
        self._nameFont = (
            self.nameFontVar.get(),
            self.nameFontSize.get()
        )

        self.labelFontVar = StringVar()
        self.labelFontVar.set( labelFont )
        self.labelFontSize = IntVar()
        self.labelFontSize.set( labelSize )
        self._labelFont = (
            self.labelFontVar.get(),
            self.labelFontSize.get()
        )

        self.valueFontVar = StringVar()
        self.valueFontVar.set( valueFont )
        self.valueFontSize = IntVar()
        self.valueFontSize.set( valueSize )
        self._valueFont = (
            self.valueFontVar.get(),
            self.valueFontSize.get()
        )



        if startDrawFunc == 'merged' :
            self.draw(
                groupFunc = self.drawMergedGroups,
                printFunc = self.printHist
            )
        elif startDrawFunc == 'automerged' :
            self.draw(
                groupFunc = self.drawAutoNestedGroups,
                printFunc = self.printHist,
                nbGroupsPerCol = 1,
                nestLevel = 1
            )
        else :
            self.draw(
                groupFunc = self.drawSplitedGroups,
                printFunc = self.printHist,
                nbGroupsPerCol = 1
            )


    def serieMeasurement( self, nestLevel = 0 ) :
        maxColValueOrLabelWidth = (   self.maxColBlockWidth / 1
                                    - self.paddingColRatio / 10
        )
        self.valuesSizes = self.getListDims(
            textList    = self.serie.values,
            font        = self.valueFont,
            maxWidth    = maxColValueOrLabelWidth,
            convertFunc = self.sep1000
        )
        self.maxValuesSize = (
            max( bboxOb[ 'width' ] for bboxOb in self.valuesSizes ),
            max( bboxOb[ 'height' ] for bboxOb in self.valuesSizes )
        )

        maxFooterWidth = maxColValueOrLabelWidth
        self.levelsSizes = []
        for levelIdx in range(
                len( self.serie.index.names ) - 1, -1, -1
        ):
            level = self.serie.index.levels[ levelIdx ]
            levelSizes = self.getListDims(
                textList    = level,
                font        = self.labelFont,
                maxWidth    = maxFooterWidth
            )

            margin = (
                self.paddingColRatio * 2
                if
                    levelIdx == len( self.serie.index.names ) - ( 1 + nestLevel )
                else
                    0
            )
            maxFooterWidth = sum(
                [ min(
                        bboxOb[ 'width' ] * ( 1 + margin ),
                        bboxOb[ 'width' ] + self.maxPaddingCol * 2
                  )
                  for bboxOb in levelSizes[ : len( levelSizes ) - ( 1 + nestLevel ) ]
                 ]
            )
            self.levelsSizes.insert( 0, levelSizes )

        self.namesSizes = self.getListDims(
            textList = self.serie.index.names,
            font     = self.nameFont,
            maxWidth = self.maxNamesWidth
        )
        self.maxNamesSizes = (
              max( bboxOb[ 'width' ] for bboxOb in self.namesSizes[ : len( self.namesSizes ) - (  nestLevel ) ] )
            * ( 1 + self.marginNamesRatio ),

            max( bboxOb[ 'height' ] for bboxOb in self.namesSizes[ : len( self.namesSizes ) - ( nestLevel ) ] )
            * ( 1 + self.marginLabelRatio ),
        )

        self.maxLevelsSizes = [
            (
                max( bboxOb[ 'width' ]  for bboxOb in levelSize ),
                max(
                    max( bboxOb[ 'height' ] * ( 1 + self.marginLabelRatio ) for bboxOb in levelSize ),
                    self.namesSizes[ lvlIdx ][ 'height' ] * ( 1 + self.marginNamesRatio )
                )
            ) for lvlIdx, levelSize in enumerate( self.levelsSizes )
        ]
        self.footerHeight = sum( [
            maxLvlSize[ 1 ] for maxLvlSize in self.maxLevelsSizes[ : len( self.maxLevelsSizes ) - nestLevel ]
        ] )
        self.headAndfootHeight = self.footerHeight + self.maxValuesSize[ 1 ]

        colWidth = max(
            self.maxValuesSize[ 0 ],
            self.maxLevelsSizes[ len( self.maxLevelsSizes ) - ( 1 + nestLevel ) ][ 0 ]
        )
        self.colWidth = colWidth + min( colWidth * self.paddingColRatio * 2, self.maxPaddingCol * 2 )
        self.colMargin = self.colWidth * self.marginColRatio
        self.colBlockWidth = self.colWidth + self.colMargin * 2

        self.valuesDelta = (
              self.serie.values.max()
            - min( self.serie.values.min(), 0 )
        )
        self.originY = 0 - min( self.serie.values.min(), 0 )
        self.groupMargin = min(
            self.colBlockWidth * self.marginGroupRatio,
            self.maxMarginGroup
        )

        self.setTicks( self.groupHeight, minTickHeight = 100 )
        self.ticksMargin = self.marginLabelRatio * max(
            [
                bboxOb[ 'width' ] for bboxOb in
                    self.getListDims(
                        textList = [
                            self.ticks[ 'ticksVal' ] * ( nTick + 1 ) for
                            nTick in range( self.ticks[ 'nbTicks' ] )
                         ],
                        font     = self.valueFont,
                        convertFunc = self.sep1000
                    )
            ]
        )

    def makeFrame( self, parent ) :
        parent.update()
        self.frameCont = Frame( parent, highlightthickness = 0 )
        self.frameCont.pack( fill = 'both', expand = 'yes', anchor = 'nw' )

        panelChilds = []
        panelSep = {
            'class' : ttk.Separator,
            'args' : [],
            'kwargs' :{
                'orient':'horizontal'
            }
        }
        self.picHist = PhotoImage( file = Path( 'lib/images/histo.gif', format = 'gif' ) )
        self.picHistG = PhotoImage( file = Path( 'lib/images/histoG.gif', format = 'gif' ) )
        self.picGraph = PhotoImage( file = Path( 'lib/images/graph.gif', format = 'gif' ) )
        self.picGraphG = PhotoImage( file = Path( 'lib/images/graphG.gif', format = 'gif' ) )
        picButWidth = ( self.maxToolPanelWidth - 20 ) / 4

        panelChilds.append(
            {
                'class' : customTk.ButtonGrid,
                'args' : [],
                'kwargs' :{
                    'width' : self.maxToolPanelWidth - 20,
                    'height' : picButWidth,
                    'nbCol' : 4,
                    'buttons' :[
                        { 'args' : [],
                          'kwargs' : {
                            'image' : self.picHist,
                            'command': self.changeToHist
                          }
                        },
                        { 'args' : [],
                          'kwargs' : {
                            'image' : self.picHistG,
                            'command': self.changeToHistG
                          }
                        },
                        { 'args' : [],
                          'kwargs' : {
                            'image' : self.picGraph,
                            'command': self.changeToGraph
                           }
                          },
                        { 'args' : [],
                          'kwargs' : {
                            'image' : self.picGraphG,
                            'command': self.changeToGraphG
                          }
                        },

                    ]
                }
            }
        )
        panelChilds.append( panelSep )

        panelChilds.append(
                {
                    'class' : customTk.fieldIncrement,
                    'args' : [],
                    'kwargs' :{
                        'text' : 'Hauteur des graphs',
                        'tkVar'  : self.groupHeightVar,
                        'width' : self.maxToolPanelWidth - 20,
                        'height': 50,
                        'onchange' : self.updateGroupHeight,
                        'min' : 100,
                        'max' : 2000,
                        'incValue' : 50
                    }
                }
            )
        panelChilds.append( panelSep )
        panelChilds.append(
                {
                    'class' : customTk.FontSelect,
                    'args' : [],
                    'kwargs' :{
                        'title' : 'Police des entêtes',
                        'tkNameVar'  : self.nameFontVar,
                        'tkSizeVar'  : self.nameFontSize,
                        'width' : self.maxToolPanelWidth - 20,
                        'height': 50,
                        'onchange' : self.updateNameFont,
                        'min' : 4,
                        'max' : 30,
                        'incValue' : 1
                    }
                }
            )
        panelChilds.append( panelSep )
        panelChilds.append(
                {
                    'class' : customTk.FontSelect,
                    'args' : [],
                    'kwargs' :{
                        'title' : 'Police des pieds de colonne',
                        'tkNameVar'  : self.labelFontVar,
                        'tkSizeVar'  : self.labelFontSize,
                        'width' : self.maxToolPanelWidth - 20,
                        'height': 50,
                        'onchange' : self.updateLabelFont,
                        'min' : 4,
                        'max' : 30,
                        'incValue' : 1
                    }
                }
            )
        panelChilds.append( panelSep )
        panelChilds.append(
                {
                    'class' : customTk.FontSelect,
                    'args' : [],
                    'kwargs' :{
                        'title' : 'Police des valeurs',
                        'tkNameVar'  : self.valueFontVar,
                        'tkSizeVar'  : self.valueFontSize,
                        'width' : self.maxToolPanelWidth - 20,
                        'height': 50,
                        'onchange' : self.updateValueFont,
                        'min' : 4,
                        'max' : 30,
                        'incValue' : 1
                    }
                }
            )
        panelChilds.append( panelSep )


        self.panelCont = customTk.ScrollWrapper(
            self.frameCont,
            orient = 'y',
            anchors = 'ne',
            width = self.maxToolPanelWidth - 20,
            wdgtCLass = Frame,
            wdgtKwargs = {
                'bd' : 0,
                'highlightthickness' : 0,
                'bg' : '#9f17c8',
                'width' : self.maxToolPanelWidth - 20
            },
            children = panelChilds
        )

        self.panelCont.pack( side = 'left', fill = 'y', expand = 'no', anchor = 'nw' )

        panelSep = customTk.LargeSep( self.frameCont, orient = "vertical", width = 10 )
        panelSep.pack( side = 'left', expand = 'no', fill = 'y', anchor = 'nw' )

        self.canvasPanel = Frame( self.frameCont, highlightthickness = 0 )

        self.canvasFrame = Frame( self.canvasPanel, highlightthickness = 0 )
        lengendFrameHeight = 200
        self.legendFrame = Frame( self.canvasPanel, height = lengendFrameHeight, highlightthickness = 0 )
        self.legendFrame.pack( side ='bottom', expand = 'yes', fill = 'both', anchor = 'nw'  )

        lengendSep = customTk.LargeSep( self.canvasPanel, orient = "horizontal", height = 10 )
        lengendSep.pack( side = 'bottom', expand = 'no', fill = 'x', anchor = 'nw' )

        self.canvasFrame.pack( side ='top', expand = 'yes', fill = 'both', anchor = 'nw' )

        self.canvasPanel.pack( side ='right', expand = 'yes', fill = 'both', anchor = 'nw' )

        self.canvasCont = Frame( self.canvasFrame )
        self.canvasCont.pack( side = 'right', expand = 'yes', fill = 'both', anchor = 'nw' )

        panelSep.bind( "<B1-Motion>", self.resizeToolPanel )
        lengendSep.bind( "<B1-Motion>", self.resizeLegendPanel )

        self.legendScrollWrap = customTk.ScrollWrapper(
            self.legendFrame,
            orient = 'y',
            anchors = 'ne',
            wdgtCLass = Canvas,
            wdgtKwargs = {
                'bd' : 0,
                'bg' : self.canvasBackground,
                'highlightthickness' : 0,
                'height' : lengendFrameHeight
            }
        )
        self.legendCanvas = self.legendScrollWrap.canvas
        self.legendScrollWrap.pack( side = 'top', expand = 'yes', fill = 'both', anchor = 'nw' )

        self.legendScrollWrap.config( width = 300 )
        self.legendScrollWrap.update()
        self.panelCont.config( height = 300 )
        self.panelCont.update()

        self.frameCont.event_generate( "<B1-Motion>", x = 300 )
        self.legendFrame.event_generate( "<B1-Motion>", y = 300 )

    def setupCanvas( self, nestLevel = 0 ) :

        self.serieMeasurement( nestLevel = nestLevel )
        self.buildGroups()
        self.columnsContentStore = {}
        self.curvesStore = {}

        if hasattr( self, 'canvas' ) == False :

            self.makeFrame( self.parent )
            self.frameCont.update()

            cont = self.canvasCont
            self.parent.bind("<Configure>", self.onResize)
            self.canvas = Canvas(
                cont, bd = 0, bg = self.canvasBackground,
                highlightthickness = 0
            )
            self.canvas.overIdx = None
            self.canvas.labelRect = None
            self.canvas.labelText = None
            vsb = ttk.Scrollbar(
                cont, orient = "vertical", command = self.canvas.yview
            )
            hsb = ttk.Scrollbar(
                cont, orient = "horizontal", command = self.canvas.xview
            )

            self.canvas.configure(
                yscrollcommand = vsb.set, xscrollcommand = hsb.set
            )

            vsb.pack( side = 'right', fill = 'y' )
            hsb.pack( side = 'bottom', fill = 'x' )
            self.canvas.pack( anchor = "nw" )
            #cont.pack( fill = BOTH, expand = YES )
            self.canvas.bind( "<Motion>", self.onCanvasOver )
            self.canvas.bind( "<Button-1>", self.onCanvasPress )
            self.canvas.bind( "<B1-Motion>", self.onDragCanvas )

            if self.system == 'Linux' :
                self.canvas.bind(
                    "<Button-4>", self.onCanvasMousewheelX11
                )
                self.canvas.bind(
                    "<Button-5>", self.onCanvasMousewheelX11
                )
            else :
                self.canvas.bind(
                    "<MouseWheel>", self.onCanvasMousewheel
                )

        self.canvas.delete( 'all' )
        self.canvas.config(
            width = self.parent.winfo_width(),
            height = self.parent.winfo_height()
        )

    def buildGroups( self ) :
        self.generateRandomLevelsColors()
        self.serieItems = tuple( self.serie.items() )
        self.chartGroups = {
            'groups'        : [],
            'maxGroupWidth' : 0
        }
        self.valuesIterCt = 0
        self.buildLvlGrp( self.chartGroups[ 'groups' ], 0 )
        del self.valuesIterCt

        for group in self.chartGroups[ 'groups' ] :
            self.chartGroups[ 'maxGroupWidth' ] = max(
                self.chartGroups[ 'maxGroupWidth' ],
                group[ 'width' ]
        )

    def buildLvlGrp( self, parentGrp, lvlIdx, parentOb = None,
        pathList = None
    ) :
        lvl = self.serie.index.levels[ lvlIdx ]
        isValueLvl = lvlIdx == len( self.serie.index.levels ) - 1
        if pathList == None :
            pathList = []
        for i in range( len( lvl ) ) :
            obPath = pathList.copy() + [ lvl[ i ] ]
            if isValueLvl == False :
                newGrp = {
                    'groups' : [],
                    'idxName': lvlIdx,
                    'idxCode': i,
                    'width'  : 0,
                    'isFake' : True,
                    'pos'    : self.serie.index.levels[ lvlIdx ].get_loc( obPath[ ::-1 ][ 0 ] )
                }
                parentGrp.append( newGrp )
                self.buildLvlGrp( newGrp[ 'groups' ], lvlIdx + 1, parentOb = newGrp, pathList =  obPath )
                if parentOb != None :
                    if newGrp[ 'isFake' ] == False :
                        parentOb[ 'isFake' ] = False
                    parentOb[ 'width' ] += newGrp[ 'width' ]
                newGrp[ 'groups' ].sort( key = lambda k : k[ 'idxCode' ] )

            else :
                isSamePath = True
                if self.valuesIterCt >= len( self.serie.values ) :
                    isSamePath = False
                else :
                    indexTuple, valueItem = self.serieItems[ self.valuesIterCt ]
                    for i in range( len( indexTuple ) ) :
                        if indexTuple[ i ] != obPath[ i ] :
                            isSamePath = False
                            break

                newValue = {
                    'idxName' : lvlIdx,
                }
                if isSamePath :
                    newValue[ 'value' ] = valueItem
                    newValue[ 'idxCode' ] = self.serie.index.codes[ lvlIdx ][ self.valuesIterCt ]
                    newValue[ 'idxVal' ] = self.valuesIterCt
                    self.valuesIterCt += 1
                    if parentOb != None :
                        parentOb[ 'isFake' ] = False
                else :
                    newValue[ 'value' ] = 0
                    newValue[ 'idxCode' ] = self.serie.index.levels[ lvlIdx ].get_loc( obPath[ ::-1 ][ 0 ] )
                    newValue[ 'idxVal' ] = -1
                    newValue[ 'isFake' ] = True

                    if parentOb[ 'isFake' ] == False :
                        parentOb[ 'hasFake' ] = True
                parentGrp.append( newValue )
                parentOb[ 'width' ] += self.colBlockWidth

    def draw( self, groupFunc = None, printFunc = None,
        nbGroupsPerCol = None, nestLevel = None
    ) :
        if groupFunc != None : self.curGroupFunc = groupFunc
        if printFunc != None : self.curPrintFunc = printFunc
        if nbGroupsPerCol != None : self.curNbGroupsPerCol = nbGroupsPerCol
        if nestLevel != None : self.curNestLevel = nestLevel

        self.points = {}
        self.setupCanvas( nestLevel = self.curNestLevel )
        self.drawLegend()
        self.curGroupFunc(
            self.curPrintFunc, nbGroupsPerCol = self.curNbGroupsPerCol,
            nestLevel = self.curNestLevel
        )

    def drawDataGroups( self, nbGroupsPerCol, nbRows,
        printFunc, offsetColorLevel = 1
    ) :
        totalWidth = (
              nbGroupsPerCol * self.chartGroups[ 'maxGroupWidth' ]
            + ( nbGroupsPerCol + 1 ) * self.groupMargin
            + self.maxNamesSizes[ 0 ]
        )
        totalHeight = (
              nbRows * ( self.groupHeight + self.headAndfootHeight )
            + ( nbRows + 1 ) * self.groupMargin
        )
        self.canvas.configure(
            scrollregion = ( 0 , 0, totalWidth, totalHeight )
        )
        incrX = 1 if nbGroupsPerCol > 1 else 0
        incrY = 1 if nbRows > 1 else 0
        for idx, group in enumerate( self.chartGroups[ 'groups' ] ) :
            posx = ( idx % nbGroupsPerCol ) * incrX
            posy = math.floor( idx / nbGroupsPerCol ) * incrY
            bottom = (   self.groupMargin
                       + self.groupHeight + self.headAndfootHeight
                       + (   posy * ( self.groupHeight + self.headAndfootHeight )
                           + ( posy * self.groupMargin )
                       )
            )
            left = (   self.groupMargin
                     + (   posx * self.chartGroups[ 'maxGroupWidth' ]
                         + ( posx * self.groupMargin )
                       )
            )
            if posx == 0 :
                nameBottom = bottom
                for idxName, name in enumerate( self.serie.index.names ) :
                    nameDict = {
                        'text'   : str( name ),
                        'anchor' : 'w',
                        'font'   : self.nameFont
                    }
                    if self.namesSizes[ idxName ][ 'maxWidth' ] != None :
                        nameDict[ 'width' ] = self.namesSizes[ idxName ][ 'maxWidth' ]
                    self.canvas.create_text(
                        left,
                        nameBottom - self.maxLevelsSizes[ idxName ][ 1 ] / 2,
                        **nameDict
                    )
                    nameBottom -= self.maxLevelsSizes[ idxName ][ 1 ]

                for nTick in range( self.ticks[ 'nbTicks' ] + 1 ) :
                    self.canvas.create_text(
                        left + self.maxNamesSizes[ 0 ] - self.ticksMargin,
                        bottom - self.footerHeight - ( nTick ) * self.ticks[ 'tickHeight' ],
                        text = self.sep1000( self.ticks[ 'ticksVal' ] * ( nTick ) ),
                        anchor = "e",
                        font = self.valueFont
                    )

            left += self.maxNamesSizes[ 0 ]

            self.canvas.create_rectangle(
                left,
                bottom,
                left + self.chartGroups[ 'maxGroupWidth' ],
                bottom - self.maxLevelsSizes[ 0 ][ 1 ]
            )

            self.drawGroup(
                group = group,
                cv = self.canvas,
                bl = ( left, bottom ),
                tr = ( left + self.chartGroups[ 'maxGroupWidth' ],
                       bottom - (self.groupHeight + self.headAndfootHeight )
                )
            )
        printFunc( offsetColorLevel = offsetColorLevel)

    def drawAutoNestedGroups( self, printFunc, nbGroupsPerCol, nestLevel = 1 ) :
        rowsDiv = math.floor(
              len( self.chartGroups[ 'groups' ] )
            / nbGroupsPerCol
        )
        nbRows = (
              rowsDiv
            + (   1 if len( self.chartGroups[ 'groups' ] )
                % ( rowsDiv * nbGroupsPerCol ) > 0 else 0
              )
        )
        nbLevels = len( self.serie.index.names )
        mergeIndex = nbLevels - nestLevel
        firstMergedGroup = self.chartGroups
        for i in range( mergeIndex ) :
            firstMergedGroup = firstMergedGroup[ 'groups' ][ 0 ]


        #mergedGroupWidth = firstMergedGroup[ 'width' ]
        #mergedGroupWidth = self.maxLevelsSizes[ mergeIndex - 1 ][ 0 ]
        mergedGroupWidth = self.colBlockWidth
        levelsLen = []
        curGrp = self.chartGroups
        for i in range( mergeIndex ) :
            levelsLen.append( len( curGrp[ 'groups' ] ) )
            curGrp = curGrp[ 'groups' ][ 0 ]
        levelsWidth = [ 0 ] * ( mergeIndex )
        levelsWidth[ len( levelsWidth ) - 1 ] = mergedGroupWidth
        for i in range( len( levelsWidth ) - 2, -1, -1 ) :
            levelsWidth[ i ] = levelsWidth[ i + 1 ] * levelsLen[ i + 1 ]
        totalWidth = (
              nbGroupsPerCol * levelsWidth[ 0 ]
            + ( nbGroupsPerCol + 1 ) * self.groupMargin
            + self.maxNamesSizes[ 0 ]
        )
        totalHeight = (
              nbRows * ( self.groupHeight + self.headAndfootHeight )
            + ( nbRows + 1 ) * self.groupMargin
        )
        self.canvas.configure(
            scrollregion = ( 0 , 0, totalWidth, totalHeight )
        )
        incrX = 1 if nbGroupsPerCol > 1 else 0
        incrY = 1 if nbRows > 1 else 0
        for idx, group in enumerate( self.chartGroups[ 'groups' ] ) :
            posx = ( idx % nbGroupsPerCol ) * incrX
            posy = math.floor( idx / nbGroupsPerCol ) * incrY
            bottom = (   self.groupMargin
                       + self.groupHeight + self.headAndfootHeight
                       + (   posy * ( self.groupHeight + self.headAndfootHeight )
                           + ( posy * self.groupMargin )
                       )
            )
            left = (   self.groupMargin
                     + (   posx * levelsWidth[ 0 ]
                         + ( posx * self.groupMargin )
                       )
            )
            if posx == 0 :
                nameBottom = bottom
                for idxName, name in enumerate( self.serie.index.names ) :
                    if idxName == mergeIndex : break
                    nameDict = {
                        'text'   : str( name ),
                        'anchor' : 'w',
                        'font'   : self.nameFont
                    }
                    if self.namesSizes[ idxName ][ 'maxWidth' ] != None :
                        nameDict[ 'width' ] = self.namesSizes[ idxName ][ 'maxWidth' ]
                    self.canvas.create_text(
                        left,
                        nameBottom - self.maxLevelsSizes[ idxName ][ 1 ] / 2,
                        **nameDict
                    )
                    nameBottom -= self.maxLevelsSizes[ idxName ][ 1 ]

                for nTick in range( self.ticks[ 'nbTicks' ] + 1 ) :
                    self.canvas.create_text(
                        left + self.maxNamesSizes[ 0 ] - self.ticksMargin,
                        bottom - self.footerHeight - ( nTick ) * self.ticks[ 'tickHeight' ],
                        text = self.sep1000( self.ticks[ 'ticksVal' ] * ( nTick ) ),
                        anchor = "e",
                        font = self.valueFont
                    )

            self.drawNestedGroupsContainer(
                group = group,
                left = left + self.maxNamesSizes[ 0 ],
                bottom = bottom,
                top = bottom - ( self.groupHeight + self.headAndfootHeight ),
                curLvl = 0,
                nestLevel = mergeIndex,
                mergedGroupWidth = mergedGroupWidth,
                levelsWidth = levelsWidth
            )
            left += self.maxNamesSizes[ 0 ]

        #self.drawNestedGroups( nbGroupsPerCol, nbRows, printFunc, curLvl = 0, nestLevel = 2 )
        printFunc()

    def drawNestedGroupsContainer( self, group, left, bottom, top, curLvl, nestLevel, mergedGroupWidth, levelsWidth ) :

        self.canvas.create_line(
            left,
            bottom,
            left + levelsWidth[ curLvl ],
            bottom,
            left + levelsWidth[ curLvl ],
            bottom - self.maxLevelsSizes[ curLvl ][ 1 ],
            left,
            bottom - self.maxLevelsSizes[ curLvl ][ 1 ],
            left,
            bottom
        )
        self.canvas.create_text(
            left + levelsWidth[ curLvl ] / 2,
            bottom - self.maxLevelsSizes[ curLvl ][ 1 ] / 2,
            text = self.serie.index.levels[ curLvl ][ group[ 'idxCode' ] ],
            anchor = "c",
            font = self.labelFont
        )
        #curLvl += 1
        #bottom -= self.maxLevelsSizes[ curLvl ][ 1 ]
        nextLvl = curLvl + 1
        if nextLvl < nestLevel :
            self.canvas.create_line(
                left,
                bottom - self.footerHeight,
                left,
                top
            )
            for gIdx, subGroup in enumerate( group[ 'groups' ] ) :
                self.drawNestedGroupsContainer(
                    group = subGroup,
                    left = left + levelsWidth[ nextLvl ] * gIdx,
                    bottom = bottom - self.maxLevelsSizes[ curLvl ][ 1 ],
                    top = top,
                    curLvl = nextLvl,
                    nestLevel = nestLevel,
                    mergedGroupWidth = mergedGroupWidth,
                    levelsWidth = levelsWidth
                )

        else :

            self.setColumnGeometry(
                group = group,
                left = left,
                bottom = bottom  ,
                right = left + self.colBlockWidth,
                top = top,
                curLvl = curLvl,
                maxLevelSize = self.maxLevelsSizes[ group[ 'idxName' ] ],
                levelsWidth = levelsWidth
            )

    def setColumnGeometry( self,
        group, left, bottom, right, top, maxLevelSize, curLvl, levelsWidth
    ) :
        baseY = bottom - maxLevelSize[ 1 ]
        #avHeight = baseY - ( tr[ 1 ] + self.maxValuesSize[ 1 ] )


        for t in range( 0, self.ticks[ 'nbTicks' ] ) :
            self.canvas.create_line(
                left,
                baseY - ( t + 1 ) * self.ticks[ 'tickHeight' ],
                right,
                baseY - ( t + 1 ) * self.ticks[ 'tickHeight' ]
            )

        for valueEl in group[ 'groups' ] :
            top = (
                  baseY
                - ( valueEl[ 'value' ] / self.valuesDelta ) * self.groupHeight
            )
            self.canvas.create_text(
                left + ( right - left ) / 2 ,
                top,
                anchor = "s",
                font   = self.valueFont,
                text   = self.sep1000( valueEl[ 'value' ] )
            )


            self.addToColumnsStore(
                left    = left,
                bottom  = baseY,
                right   = right,
                top     = top,
                value   = valueEl[ 'value'   ],
                idxVal  = valueEl[ 'idxVal'  ],
                idxName = valueEl[ 'idxName' ],
                idxCode = valueEl[ 'idxCode' ],
                labels  = None
            )


    def drawNestedGroup( self, printFunc ):
        a = 0

    def drawSplitedGroups( self, printFunc, nbGroupsPerCol, nestLevel ) :
        rowsDiv = math.floor(
              len( self.chartGroups[ 'groups' ] )
            / nbGroupsPerCol
        )
        nbRows = (
              rowsDiv
            + (   1 if len( self.chartGroups[ 'groups' ] )
                % ( rowsDiv * nbGroupsPerCol ) > 0 else 0
              )
        )
        self.drawDataGroups( nbGroupsPerCol, nbRows, printFunc )

    def drawMergedGroups( self, printFunc, **kwargs ) :
        self.setupCanvas()
        self.drawDataGroups( 1, 1, printFunc, offsetColorLevel = 2 )

    def drawGroup( self, group, cv, bl, tr, writeLabels = True,
        grpIterCt = None, parentIdx = None, parentColor = None, **kwargs
    ) :
        nameVal = (
            self.serie.index.levels
                [ group[ 'idxName' ] ][ group[ 'idxCode' ] ]
        )
        levelLabelBboxOb = (
            self.levelsSizes[ group[ 'idxName' ] ][ group[ 'idxCode' ] ]
        )
        maxLevelSize = (
            self.maxLevelsSizes[ group[ 'idxName' ] ]
        )

        textPos = (
            bl[ 0 ] + ( tr[ 0 ] - bl[ 0 ] ) / 2,
            bl[ 1 ] - maxLevelSize[ 1 ] / 2
        )

        renderText = (
            group[ 'plainText' ] if 'plainText' in group else nameVal
        )

        textParams = {
            'anchor' : "c",
            'font'   : self.labelFont,
            'text'   : str( renderText )
        }
        if levelLabelBboxOb[ 'maxWidth' ] != None :
            textParams[ 'width' ] = levelLabelBboxOb[ 'maxWidth' ]

        if writeLabels :
            labelText = cv.create_text(
                *textPos,
                **textParams
            )
            cv.create_rectangle(
                bl[ 0 ],
                bl[ 1 ],
                tr[ 0 ],
                bl[ 1 ] - maxLevelSize[ 1 ]
            )

        if 'groups' in group :
            gW = ( tr[ 0 ] - bl[ 0 ] ) / len( group[ 'groups' ] )
            childGroupidxName = group[ 'groups' ][ 0 ][ 'idxName' ]
            childGroupLevels = (
                self.serie.index.levels[ childGroupidxName ]
            )
            gW = ( tr[ 0 ] - bl[ 0 ] ) / len( childGroupLevels )
            grpIterCt = 0;
            for  levelCode, levelName in enumerate( childGroupLevels ) :
                bottom = bl[ 1 ] - maxLevelSize[ 1 ]
                left = bl[ 0 ] + levelCode * gW

                if  ( grpIterCt < len( group[ 'groups' ] )
                    and ( group[ 'groups' ]
                            [ grpIterCt ][ 'idxCode' ]
                        )
                    == levelCode
                ) :
                    self.drawGroup(
                        group = ( group[ 'groups' ]
                                    [ grpIterCt ]
                        ),
                        cv          = cv,
                        bl          = ( left, bottom ),
                        tr          = ( left + gW, tr[ 1 ] ),
                        writeLabels = writeLabels,
                        grpIterCt  = grpIterCt,
                        parentIdx = group[ 'idxCode' ],
                        parentColor = self.levelsColors[ group[ 'idxName' ] ][ group[ 'idxCode' ] ]
                    )
                    grpIterCt += 1
                else :
                    self.drawGroup(
                        group = {
                            'plainText' : levelName,
                            'idxCode'   : levelCode,
                            'idxName'   : childGroupidxName,
                            'parentIdx' : group[ 'idxCode' ],
                            'parentColor' : self.levelsColors[ group[ 'idxName' ] ][ group[ 'idxCode' ] ]
                        },
                        cv          = cv,
                        bl          = ( left, bottom ),
                        tr          = ( left + gW, tr[ 1 ] ),
                        writeLabels = writeLabels
                    )

        elif 'value' in group :
            if parentIdx not in self.points :
                self.points[ parentIdx ] = []
            pts = self.points[ parentIdx ]
            baseY = bl[ 1 ] - maxLevelSize[ 1 ]
            #avHeight = baseY - ( tr[ 1 ] + self.maxValuesSize[ 1 ] )
            top = (
                  baseY
                - ( group[ 'value' ] / self.valuesDelta ) * self.groupHeight
            )

            for t in range( 0, self.ticks[ 'nbTicks' ] ) :
                cv.create_line(
                    bl[ 0 ],
                    baseY - ( t + 1 ) * self.ticks[ 'tickHeight' ],
                    tr[ 0 ],
                    baseY - ( t + 1 ) * self.ticks[ 'tickHeight' ]
                )
            pts.append( {
                'left' : bl[ 0 ] + ( tr[ 0 ] - bl[ 0 ] ) / 2,
                'top' : top,
                'color' : parentColor
            } )
            cv.create_text(
                bl[ 0 ] + ( tr[ 0 ] - bl[ 0 ] ) / 2 ,
                top,
                anchor = "s",
                font   = self.valueFont,
                text   = self.sep1000( group[ 'value' ] )
            )

            self.addToColumnsStore(
                left    = bl[ 0 ],
                bottom  = baseY,
                right   = tr[ 0 ],
                top     = top,
                value   = group[ 'value'   ],
                idxVal  = group[ 'idxVal'  ],
                idxName = group[ 'idxName' ],
                idxCode = group[ 'idxCode' ],
                labels  = None
            )
            if grpIterCt == 0 :
                cv.create_line(
                    bl[ 0 ],
                    baseY,
                    bl[ 0 ],
                    baseY - ( self.groupHeight + self.maxValuesSize[ 1 ] )
                )
            #self.points.append( pts )


    def printHist( self, offsetColorLevel = 1 ) :
        if hasattr( self, 'rectValues' ) == False :
            self.rectValues = {}
        for columnKey in self.columnsContentStore.keys() :
            columnList = self.columnsContentStore[ columnKey ]
            columnList[ 'content' ] = sorted(
                columnList[ 'content' ],
                key = lambda k : k[ 'value' ]
            )
            left    = columnList[ 'left'   ]
            offsetY = columnList[ 'bottom' ]
            for rect in columnList[ 'content' ] :
                if rect[ 'value' ] > 0 :
                    targetlevelIdx = len( self.levelsColors ) - offsetColorLevel
                    code = self.serie.index.codes[ targetlevelIdx ][ rect[ 'idxVal' ] ]
                    color = self.levelsColors[ targetlevelIdx ][ code ]
                    rectShape = self.canvas.create_rectangle(
                        left,
                        offsetY,
                        rect[ 'right' ],
                        rect[ 'top' ],
                        fill = color,
                        outline = "",
                        tag = str( rect[ 'idxVal' ] )
                    )
                    self.rectValues[ rectShape ] = rect
                    offsetY = rect[ 'top' ]

    def printCurve2( self, offsetColorLevel = 2 ) :
        graphsSore = {}
        for columnKey in self.columnsContentStore.keys() :
            columnList = self.columnsContentStore[ columnKey ]

    def printCurve( self, offsetColorLevel = 2 ) :
        self.lines = {}
        if len( self.columnsContentStore[ list( self.columnsContentStore.keys() )[ 0 ] ][ 'content' ] ) > 1 :
            for columnKey in self.columnsContentStore.keys() :
                columnList = self.columnsContentStore[ columnKey ]
                columnList[ 'content' ] = sorted(
                    columnList[ 'content' ],
                    key = lambda k : k[ 'value' ]
                )
                left    = columnList[ 'left'   ]
                for rect in columnList[ 'content' ] :
                    targetlevelIdx = len( self.levelsColors ) - offsetColorLevel
                    code = self.serie.index.codes[ targetlevelIdx ][ rect[ 'idxVal' ] ]
                    nameLevel = self.serie.index.levels[ targetlevelIdx ][ code ]
                    if nameLevel not in self.lines :
                        self.lines[ nameLevel ] = {
                            'points' : [],
                            'color' : self.levelsColors[ targetlevelIdx ][ code ]
                        }
                    self.lines[ nameLevel ][ 'points' ].append(
                        left + ( rect[ 'right' ] - left ) / 2
                    )
                    self.lines[ nameLevel ][ 'points' ].append(
                        rect[ 'top' ]
                    )
            for line in self.lines.values() :
                self.canvas.create_line( *tuple( line[ 'points' ] ), fill = line[ 'color' ], width = 4, smooth = 0, activewidth = 8 )
        else :

            for line in self.points.values() :
                pts = []
                col = None
                for pt in line :
                    pts.append( pt[ 'left' ] )
                    pts.append( pt[ 'top' ] )
                    col = pt[ 'color' ]


                self.canvas.create_line( *tuple( pts ), fill = col, width = 4, smooth = 0, activewidth = 8 )



    def clearCanvasLabel( self, *args, **kwargs ) :
        if self.canvas.labelRect :
            self.canvas.delete( self.canvas.labelRect )
            self.canvas.delete( self.canvas.labelText )
            self.canvas.labelRect = None
            self.canvas.labelText = None
            self.canvas.overIdx = None

    def onResize( self, event ) :
        self.canvas.config(
            width = self.parent.winfo_width(),
            height = self.parent.winfo_height()
        )

    def onCanvasPress( self, event ) :
        self.canvas.scan_mark(event.x, event.y)

    def onDragCanvas( self, event ) :
        self.canvas.scan_dragto( event.x, event.y, gain = 1 )

    def onCanvasOver( self, event ) :
        hoverObjs = self.canvas.find_overlapping(
            self.canvas.canvasx( event.x ),
            self.canvas.canvasy( event.y ),
            self.canvas.canvasx( event.x ) + 1,
            self.canvas.canvasy( event.y ) + 1
        )
        if len( hoverObjs ) :
            obFound = False
            for obIdx in hoverObjs :
                if obIdx in self.rectValues :
                    obFound = True
                    if obIdx != self.canvas.overIdx :
                        ob = self.rectValues[ obIdx ]
                        self.clearCanvasLabel()
                        self.canvas.labelRect = self.canvas.create_rectangle(
                            self.canvas.canvasx( event.x ),
                            self.canvas.canvasy( event.y ),
                            self.canvas.canvasx( event.x ) + 350,
                            self.canvas.canvasy( event.y ) + 125,
                            fill = '#262626',
                            tag = 'labelRect'
                        )
                        textStr = ""
                        for idx, code in enumerate( self.serie.index.codes ) :
                            textStr += '{} : {} \n'.format(
                                self.serie.index.names[ idx ],
                                self.serie.index.levels[ idx ][ self.serie.index.codes[ idx ][ ob[ 'idxVal' ] ] ]
                            )
                        textStr += 'Valeur : {}'.format( ob[ 'value' ] )
                        self.canvas.labelText = self.canvas.create_text(
                            self.canvas.canvasx( event.x ) + 5,
                            self.canvas.canvasy( event.y ) + 5,
                            text = textStr,
                            width = 300,
                            fill = '#C8C8C8',
                            font = self.valueFont,
                            tag = 'labelText',
                            anchor = 'nw'
                        )
                        break
            if obFound == False :
                self.clearCanvasLabel()
        else :
            self.clearCanvasLabel()

    def resizeToolPanel( self, event, ptx = None ):
        x = ptx if ptx != None else event.x_root
        x = min( x, self.maxToolPanelWidth )
        posx = x - self.panelCont.winfo_rootx()
        self.panelCont.config( width = posx )
        self.panelCont.resizeContent(
            posx =   posx
                   - (   self.panelCont.winfo_width()
                       - self.panelCont.canvas.winfo_width()
                      )
            )

    def resizeLegendPanel( self, event, pty = None ) :
        y = pty if pty != None else event.y_root
        y = max( y, 600 )
        offsetY = self.legendScrollWrap.winfo_rooty() - y
        posy = offsetY + self.legendScrollWrap.winfo_height()
        self.legendScrollWrap.config( height = posy )
        self.legendScrollWrap.resizeContent(
            posy =   posy
                   - (   self.legendScrollWrap.winfo_height()
                       - self.legendScrollWrap.canvas.winfo_height()
                      )
            )

    def onCanvasMousewheel( self, event ) :
        self.canvas.yview_scroll( -1 * ( event.delta / 60 ), "units" )

    def onCanvasMousewheelX11( self, event ) :
        delta = 1 if event.num == 4 else - 1
        self.canvas.yview_scroll( int( -1 * ( delta ) ), "units" )

    def getListDims( self, textList = [],
                        font = None, maxWidth = None,
                        convertFunc = None
    ) :
        ret = []
        testCanvas = Canvas( self.parent, width = 256, height = 256 )
        for text in textList :
            bboxOb = { 'maxWidth' : None }
            txt = convertFunc( text ) if convertFunc != None else str( text )
            bbox = testCanvas.bbox(
                testCanvas.create_text(
                    0, 0, anchor = "ne", font = font, text = txt
                )
            )
            if maxWidth != None :
                width = bbox[ 2 ] - bbox[ 0 ]
                if width > maxWidth :
                    bbox = testCanvas.bbox(
                        testCanvas.create_text(
                            0, 0, anchor = "ne", font = font,
                            text = txt, width = maxWidth
                        )
                    )
                    bboxOb[ 'maxWidth' ] = maxWidth

            bboxOb[ 'width' ] = bbox[ 2 ] - bbox[ 0 ]
            bboxOb[ 'height' ] = bbox[ 3 ] - bbox[ 1 ]
            ret.append( bboxOb )
        testCanvas.destroy()
        return ret

    def addToColumnsStore(  self, left, bottom, right, top,
                            value, idxVal, idxName, idxCode, labels = None
    ) :
        idString = "{}.{}".format( left, bottom )
        if idString not in self.columnsContentStore :
            self.columnsContentStore[ idString ] = {
                'left'      : left,
                'bottom'    : bottom,
                'content'   : []
            }


        store = self.columnsContentStore[ idString ]
        obStore = {
            'right'   : right,
            'top'     : top,
            'idxVal'  : idxVal,
            'idxName' : idxName,
            'idxCode' : idxCode,
            'value'   : value
        }
        if labels != None :
            obStore[ 'labels' ] = labels
        store[ 'content' ].append( obStore )

    def generateRandomColors(
        self, nbColors, nbHuePerTurn = 6, startHue = 0,
        minVal = 0.5, maxVal = 0.75,
        sat = 0.5
    ) :
        nbHueTurn = math.ceil( nbColors / nbHuePerTurn )
        hueStep = 1 / nbHuePerTurn
        hueOffsetPerTurn = hueStep / nbHueTurn
        nbValTurn = ( maxVal - minVal ) / nbHueTurn
        valStep = ( maxVal - minVal ) / nbHueTurn
        ret = []
        for i in range( nbColors ) :
            hueTurn = math.floor( i / nbHuePerTurn )

            hueCurStep = i % nbHuePerTurn
            hue = (   startHue
                    + hueTurn * hueOffsetPerTurn
                    + hueCurStep * hueStep
            ) % 1
            tsat = minVal + hueTurn * valStep
            val = maxVal - hueTurn * valStep
            ret.append(
                [
                    '#{:02x}{:02x}{:02x}'.format(
                        *(int( i * 255 ) for i in colorsys.hsv_to_rgb(
                                                    hue,
                                                    tsat,
                                                    val
                                                ))
                    )
                ]
            )
        return ret

    def generateRandomLevelsColors( self ) :
        self.levelsColors = [
            self.generateRandomColors( len( level ) )
            for level in self.serie.index.levels
        ]

    def setTicks( self, height, minTickHeight = 50 ) :
        maxNbTicks = math.floor( height / minTickHeight )
        nbDigitsToMaxVal = len( str( self.valuesDelta ) )
        ticksVal = None
        nbTicks = None
        curFloor = 1
        for digit in range( 1, nbDigitsToMaxVal + 1 ) :
            curFloor *= 10
            for digitMultiplyer in range( 1, 11 ) :
                tickUnitVal = curFloor * digitMultiplyer
                tickVal = tickUnitVal
                if tickVal * (maxNbTicks + 1) >= self.valuesDelta :
                    ticksVal = tickVal
                    nbTicks  = math.floor( self.valuesDelta / tickVal )

                if ticksVal != None : break
            if ticksVal != None : break

        self.ticks = {
            'ticksVal'   : ticksVal,
            'nbTicks'    : nbTicks,
            'tickHeight' : height * ( ticksVal / self.valuesDelta )
        }

    def sep1000( self, num ) :
        return '{:,}'.format( num ).replace( ",", " ")

    def drawLegend( self ) :
        cv = self.legendScrollWrap.canvas
        cv.delete( 'all' )
        cWidth = self.legendScrollWrap.winfo_width()
        margin = 5
        posy = margin
        for idx, lvlColor in enumerate( self.levelsColors ) :
            name = self.serie.index.names[ idx ]
            level = self.serie.index.levels[ idx ]
            curMargin = margin
            txt = cv.create_text(
                curMargin, posy, text = str( name ),
                width = cWidth - curMargin, font = self.nameFont,
                anchor = 'nw'
            )
            tBbox = cv.bbox( txt )
            posy += tBbox[ 3 ] - tBbox[ 1 ] + margin
            posx = margin * 2
            cMargin = margin * 2
            for cIdx, color in enumerate( lvlColor ) :
                lvlText = cv.create_text(
                    posx, posy, text = str( level[ cIdx ] ),
                    width = cWidth - cMargin, font = self.labelFont,
                    anchor = 'nw'
                )
                ltBbox = cv.bbox( lvlText )
                leftRect = cMargin + ltBbox[ 2 ] - ltBbox[ 0 ]
                vMiddleRect = posy + ( ltBbox[ 3 ] - ltBbox[ 1 ] ) /  2
                lvlColRect = cv.create_rectangle(
                    posx + leftRect,
                    vMiddleRect - margin,
                    posx + leftRect + 40,
                    vMiddleRect + margin,
                    fill = color
                )
                colBbox = cv.bbox( lvlColRect )
                posx = posx + leftRect + 40 + margin * 4
                if posx > 600 :
                    posx = margin * 2
                    posy += margin * 4

            posy += ltBbox[ 3 ] - ltBbox[ 1 ] + margin



        self.legendScrollWrap.canvas.config(
            scrollregion = ( self.legendScrollWrap.bbox( 'all' ) )
        )

    def changeToGraphG( self ) :
        f = self.drawAutoNestedGroups if len( self.serie.index.names ) > 2 else self.drawMergedGroups
        nestLvl = 1 if len( self.serie.index.names ) > 2 else 0
        self.draw(
            groupFunc = f,
            printFunc = self.printCurve,
            nbGroupsPerCol = 1,
            nestLevel = nestLvl
        )

    def changeToGraph( self ) :
        self.draw(
            groupFunc = self.drawSplitedGroups,
            printFunc = self.printCurve,
            nbGroupsPerCol = 1,
            nestLevel = 0
        )

    def changeToHist( self ) :
        self.draw(
            groupFunc = self.drawSplitedGroups,
            printFunc = self.printHist,
            nbGroupsPerCol = 1,
            nestLevel = 0
        )

    def changeToHistG( self ) :
        f = self.drawAutoNestedGroups if len( self.serie.index.names ) > 2 else self.drawMergedGroups
        nestLvl = 1 if len( self.serie.index.names ) > 2 else 0
        self.draw(
            groupFunc = f,
            printFunc = self.printHist,
            nbGroupsPerCol = 1,
            nestLevel = nestLvl
        )

    @property
    def nameFont( self ) :
        #return '{} {}'.format( *self._nameFont )
        return font.Font( family = self._nameFont[ 0 ], size = self._nameFont[ 1 ] )

    @nameFont.setter
    def nameFont( self, nameSize ) :
        self._nameFont = nameSize

    def updateNameFont( self ) :
        self._nameFont = (
            str( self.nameFontVar.get() ),
            self.nameFontSize.get()
        )
        self.draw()

    @property
    def valueFont( self ) :
        return font.Font( family = self._valueFont[ 0 ], size = self._valueFont[ 1 ] )

    @valueFont.setter
    def valueFont( self, nameSize ) :
        self._valueFont = nameSize

    def updateValueFont( self ) :
        self._valueFont = (
            str( self.valueFontVar.get() ),
            self.valueFontSize.get()
        )
        self.draw()

    @property
    def labelFont( self ) :
        #return '{} {}'.format( *self._labelFont )
        return font.Font( family = self._labelFont[ 0 ], size = self._labelFont[ 1 ] )

    @labelFont.setter
    def labelFont( self, nameSize ) :
        self._labelFont = nameSize

    def updateLabelFont( self ) :
        self._valueFont = (
            str( self.labelFontVar.get() ),
            self.labelFontSize.get()
        )
        self.draw()


    def setFontsFamily( self, name ) :
        valSize = self._valueFont[ 1 ]
        self.valueFont = ( name, valSize )
        nameSize = self._nameFont[ 1 ]
        self.nameFont = ( name, nameSize )
        labelSize = self._labelFont[ 1 ]
        self.labelFont = ( name, labelSize )

    def updateGroupHeight( self, height ) :
        self.groupHeight = height
        self.draw()
