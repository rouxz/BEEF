import sys

from static import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from sideGui import *
from file_manager import *
from table_gui import *






# création de la vue et du conteneur
class TopWindow(QMainWindow):
	""" create a window being the main window of the gui """
	def __init__(self, core, platform = PLATFORM_WINDOWS):
		# initiate the main widget
		QMainWindow.__init__(self)
		
		self.platform = platform

		#core
		self.core = core

		# file manager
		self.fm = MyFileManager(platform)

		# init the window
		self.initTopWindow(self.fm, self.core)

		
	""" initiate the top window """
	def initTopWindow(self, fm, core):


				########################
		# Status and menu bars
		########################

		#set the status bar
		self.statusBar().showMessage('Ready')

		# set the menu bar
		exitAction = QAction('&Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(qApp.quit)

		self.menubar = self.menuBar()
		self.fileMenu = self.menubar.addMenu('&File')
		self.fileMenu.addAction(exitAction)

		#######################"
		# central widget
		########################

		self.centralWidget = CentralWidget(fm, core, self, self.statusBar(), self.platform)
		self.setCentralWidget(self.centralWidget)
		
		
		#pack the window
		self.setWindowTitle(TITLE_TOPWINDOW)

		self.show()

# ###########################################
#
#	Central widget
#
# ############################################


class CentralWidget(QWidget):
	""" a widget being the main widget within the topwindow"""
	""" this main widget will have all the required tabs and table within """
	def __init__(self, fm, core, parent, status, platform = PLATFORM_WINDOWS):
		QWidget.__init__(self, parent)
		
		# operating system
		self.platform = platform
		
		# status bar
		self.status = status

		#init the central widget
		self.initCentralWidget(fm, core)

	def initCentralWidget(self, fm, core):
		#the top grid layout and tweak it


		self.grid = QGridLayout()
		self.grid.setSpacing(GRID_LAYOUT_SPACE)

		#SIDE PANEL
		self.sidePanel = SidePanel(fm, core, self, self.status, self.platform)
		
		#######################"
		# Place all the itemes
		########################

		

		# set the tabs
		self.tabsWidget = Tabs(core, self.sidePanel, self)
		self.grid.addWidget(self.tabsWidget, 1 , 1)


		# set the title
		self.title = QLabel(self)
		self.title.setText(TITLE_TOPWINDOW)
		self.grid.addWidget(self.title, 0 , 0, 1, -1)

		# set the side panel
		self.grid.addWidget(self.sidePanel, 1, 0)

		#setting the layout
		self.setLayout(self.grid)










