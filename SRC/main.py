import sys
from database import *
from static import *
from coreengine import *
from mainGui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from os_specifity import *

# main module for launching BEEF

def main():
	print(TITLE_TOPWINDOW)
	print(TITLE_LINE)
	print("")

	#debugging
	debug = True
	
	#find platform
	system = find_system()

	# database
	db = Database(system, debug)
	# core engine to handle db
	core = Core(db, debug)

	#for testing purpose only
	#~ core.set_rfs_used("FAA")
	#~ core.get_data_CY()
	#~ core.get_data_ref()


	# for launching the ui
	app = QApplication(sys.argv)
	# topwindow of the gui
	w = TopWindow(core, system, debug)
	w.showMaximized()
	sys.exit(app.exec_())

	db.__del__()
	print(TITLE_LINE)
	print("Quiting " + PROG_LONG_NAME)
	print(TITLE_LINE)

if __name__ == "__main__":
	main()