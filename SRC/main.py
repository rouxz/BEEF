import sys
import getopt
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

	#dynamic parameters
	dynamic_param = DynamicParameters()

	# database
	db = LocalDatabase(dynamic_param)

	
	if db != None:
		# core engine to handle db
		core = Core(db, dynamic_param.debug)

		# for launching the ui
		app = QApplication(sys.argv)
		# topwindow of the gui
		w = TopWindow(core, dynamic_param)
		w.showMaximized()
		sys.exit(app.exec_())

		db.__del__()

	print(TITLE_LINE)
	print("Quiting " + PROG_LONG_NAME)
	print(TITLE_LINE)


if __name__ == "__main__":
	main()
	
