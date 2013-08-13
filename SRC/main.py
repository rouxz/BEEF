import sys
from database import *
from static import *
from coreengine import *
from mainGui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from os_specifity import *
from param import *

# main module for launching BEEF

def main():
	print(TITLE_TOPWINDOW)
	print(TITLE_LINE)
	print("")

	#debugging
	debug = True
	


	#dynamic parameters
	dynamic_param = DynamicParameters(debug)
	
	# database
	db = Database(dynamic_param.system, debug)
	
	if db != None:
		# core engine to handle db
		core = Core(db, debug)

		#for testing purpose only
		#~ core.set_rfs_used("FAA")
		#~ core.get_data_CY()
		#~ core.get_data_ref()


		# for launching the ui
		app = QApplication(sys.argv)
		# topwindow of the gui
		w = TopWindow(core, dynamic_param.system, debug)
		w.showMaximized()
		sys.exit(app.exec_())

		db.__del__()
		print(TITLE_LINE)
		print("Quiting " + PROG_LONG_NAME)
		print(TITLE_LINE)


if __name__ == "__main__":
	main()