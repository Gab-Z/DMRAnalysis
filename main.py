from lib.ODSApiPdBridgeGUI import ODSApiPdBridgeGUI
import os

gui = ODSApiPdBridgeGUI( apiUrl = 'https://opendata.paris.fr', localDirs = os.path.join( os.path.abspath( os.path.dirname( __file__ ) ), 'staticDataSheets' ) )

gui.mainloop()
