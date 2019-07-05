import tkinter as tk
import tkinter.ttk as ttk
import math

class LargeSep( tk.Frame ) :

    def __init__( self, parent, width = 0, height = 0, bg = "", highlightthickness = 0, orient = 'horizontal', bd = 0 ) :
        tk.Frame.__init__( self, parent, width = width, height = height, bg = bg, highlightthickness = highlightthickness, bd = bd )
        self.sep1 = ttk.Separator( self, orient = orient )
        self.empty = tk.Frame( self, width = width, height = height, bd = 0 )
        self.sep2 = ttk.Separator( self, orient = orient )
        sepPackProps = {
            'fill' : 'x' if orient == 'horizontal' else 'y',
            'expand' : 'yes',
            'side'  : 'top' if orient == 'horizontal' else 'left',
            'anchor': 'nw'
        }
        self.sep1.pack( **sepPackProps )
        sepPackProps[ 'anchor' ] = 'sw' if orient == 'horizontal'else 'ne'
        self.empty.pack( fill = 'both', expand = 'yes', side = sepPackProps[ 'side' ], anchor = 'nw' )
        self.sep2.pack( **sepPackProps )

    def bind( self, evType, callback ) :
        #self.sep1.bind( evType, callback )
        #self.sep2.bind( evType, callback )
        self.empty.bind( evType, callback )



class ScrollWrapper( tk.Frame ) :
    def __init__( self,
        parent, wdgtCLass = None, wdgtArgs = (),
        wdgtKwargs = {}, width = 0, height = 0, bg = "",
        highlightthickness = 0, bd = 0, orient = 'both',
        anchors = 'sw', children = []
    ) :

        tk.Frame.__init__( self,
            parent, width = width, height = height, bg = bg,
            highlightthickness = highlightthickness, bd = bd
        )
        self.canvas = None
        self.frame = None
        if wdgtCLass == tk.Canvas :
            self.canvas = wdgtCLass( self, *wdgtArgs, **wdgtKwargs )
            self.canvas.pack(
                side = 'left', fill = 'both', expand = 'yes',
                anchor = 'nw'
            )
        else :
            self.canvas = tk.Canvas(
                self, bd = 0, highlightthickness = 0,
                width = width, height = height
            )
            self.canvas.pack(
                side = 'left', fill = 'both', expand = 'yes',
                anchor = 'nw'
            )
            self.frame = wdgtCLass(
                self.canvas, *wdgtArgs, **wdgtKwargs
            )
            for child in children :
                childWidget = child[ 'class' ](
                    self.frame, *child[ 'args' ], **child[ 'kwargs' ]
                )
                childWidget.pack(
                    side = 'top', expand = 'yes', fill = 'x',
                    anchor = 'nw'
                )
            self.canvasChild = self.canvas.create_window(
                0, 0, window = self.frame, anchor = 'nw', width = width
            )
        if orient == 'x' or orient == 'both' :
            self.xbar = ttk.Scrollbar(
                self, orient = "horizontal",
                command = self.canvas.xview
            )
            self.xbar.pack(
                side = 'bottom' if anchors[ 0 ] == 's' else 'top',
                fill = 'x'
            )
            self.canvas.configure(
                xscrollcommand = self.xbar.set
            )
        if orient == 'y' or orient == 'both' :
            self.ybar = ttk.Scrollbar(
                self, orient = "vertical",
                command = self.canvas.yview
            )
            self.ybar.pack(
                side = 'left' if anchors[ 1 ] == 'w' else 'right',
                fill = 'y'
            )
            self.canvas.configure(
                yscrollcommand = self.ybar.set
            )


    def resizeContent( self, posx = None, posy = None ) :
        newSizes = {}
        if posx != None :
            newSizes[ 'width' ] = posx
        if posy != None :
            newSizes[ 'height' ] = posy
        cvbbox = self.canvas.bbox( 'all' )
        self.canvas.configure(
            **newSizes,
            scrollregion = cvbbox
        )


class fieldIncrement( tk.Frame ) :

    def __init__(
        self, parent, text = '', val = 0, incValue = 1,
        onchange = None, width = 0, height = 0, bg = None, min = 1, max = 100,
        tkVar = None, startVal = None
    ) :
        self.onchange = onchange
        self.value = tkVar if tkVar != None else tk.IntVar()
        if startVal != None : self.value.set( startVal )
        self.incValue = incValue
        self.min = min
        self.max = max

        tk.Frame.__init__( self, parent, width = width, height = height,
            highlightthickness = 2, bd = 2, bg = bg
        )

        self.label = tk.Label( self, text = text )
        self.label.grid( column = 0, row = 0, rowspan = 2, ipadx = 10, sticky = 'w' )

        sep1 = ttk.Separator( self, orient = 'vertical' )
        sep1.grid( column = 1, row = 0, rowspan = 2, sticky = 'nsew' )

        self.valLabel = tk.Label( self, textvariable = self.value )
        self.valLabel.grid( column = 2, row = 0, rowspan = 2, ipadx = 5, sticky = 'e' )

        sep2 = ttk.Separator( self, orient = 'vertical' )
        sep2.grid( column = 3, row = 0, rowspan = 2, sticky = 'nsew' )

        self.upButton = tk.Button( self, text = '+', command = self.up )
        self.upButton.grid( column = 4, row = 0, sticky = 'nsew' )

        self.downButton = tk.Button( self, text = '-', command = self.down )
        self.downButton.grid( column = 4, row = 1, sticky = 'nsew' )

        self.grid_columnconfigure( 0, weight = 8 )
        self.grid_columnconfigure( 1, weight = 1 )
        self.grid_columnconfigure( 2, weight = 2 )
        self.grid_columnconfigure( 3, weight = 1 )
        self.grid_columnconfigure( 4, weight = 1 )

    def down( self ) :
        gval = self.value.get()
        val = gval - self.incValue
        self.updateValue( val = int(val) )

    def up( self ) :
        gval = self.value.get()
        val =  gval + self.incValue
        self.updateValue( val = int(val) )

    def updateValue( self, val ):
        if val < self.min or val > self.max :
            return False
        self.value.set( val )
        if self.onchange != None :
            self.onchange( val )


class ButtonGrid( tk.Frame ) :

    def __init__( self, parent, nbCol = 2, width = 100, buttons = [],
        highlightthickness = 0, bd = 0, bg = None, height = 100
    ) :

        tk.Frame.__init__( self, parent, width = width, height = height,
            highlightthickness = 0, bd = 0, bg = None
        )

        nbRows = math.ceil( len( buttons ) / nbCol )
        for idx, but in enumerate( buttons ) :
            childWidget = tk.Button(
                self, *but[ 'args' ], **but[ 'kwargs' ],
                width = width / nbCol, height = height / nbRows
            )
            childWidget.grid(
                row = math.floor( idx / nbCol ),
                column = idx - math.floor( idx / nbCol ) * nbCol,
                sticky = 'nsew'
            )


class FontSelect( tk.Frame ) :

    def __init__( self, parent, fontName = '', fontSize = 1, max = 20, min = 6,
        height = 100, width = 100, bd = 0, bg = None, highlightthickness = 0,
        onchange = None, tkNameVar = None, tkSizeVar = None, title = "",
        incValue = 1, startSize = 10
    ) :

        tk.Frame.__init__( self, parent, width = width, height = height,
            highlightthickness = 0, bd = 0, bg = None
        )

        self.sizeVar = tkSizeVar
        self.sizeVar.set( startSize )
        self.nameVar = tkNameVar
        self.incValue = incValue
        self.max = max
        self.min = min
        self.onchange = onchange

        self.label = tk.Label( self, text = title )
        self.label.grid( column = 0, row = 0, columnspan = 3, ipadx = 10, sticky = 'w' )

        self.select = ttk.OptionMenu( self, self.nameVar, *tk.font.families(), command = self.update )
        self.select.grid( column = 0, row = 1, rowspan = 2, ipadx = 10, sticky = 'ewns' )

        self.sizeLabel = tk.Label( self, textvariable = self.sizeVar )
        self.sizeLabel.grid(
            column = 1, row = 1, rowspan = 2, ipadx = 10, sticky= 'e'
        )

        self.upButton = tk.Button( self, text = '+', command = self.up )
        self.upButton.grid( column = 2, row = 0, sticky = 'nsew' )

        self.downButton = tk.Button( self, text = '-', command = self.down )
        self.downButton.grid( column = 2, row = 1, sticky = 'nsew' )

        self.grid_columnconfigure( 0, weight = 8 )
        self.grid_columnconfigure( 1, weight = 2 )
        self.grid_columnconfigure( 2, weight = 1 )

    def down( self ) :
        gval = self.sizeVar.get()
        val = gval - self.incValue
        self.updateValue( val = int(val) )

    def up( self ) :
        gval = self.sizeVar.get()
        val =  gval + self.incValue
        self.updateValue( val = int(val) )

    def updateValue( self, val ):
        if val < self.min or val > self.max :
            return False
        self.sizeVar.set( val )
        if self.onchange != None :
            self.onchange()

    def update( self, rowControl ) :
        if self.onchange != None :
            self.onchange()
