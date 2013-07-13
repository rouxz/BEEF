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
	
	#find platform
	system = find_system()

	# database
	db = Database(system)
	# core engine to handle db
	core = Core(db)

	#for testing purpose only
	#~ core.set_rfs_used("FAA")
	#~ core.get_data_CY()
	#~ core.get_data_ref()


	#~ # for launching the ui
	#~ app = QApplication(sys.argv)
	#~ # topwindow of the gui
	#~ w = TopWindow(core)
	#~ w.show()
	#~ sys.exit(app.exec_())

	db.__del__()

if __name__ == "__main__":
	main()