import sys

from static import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from sideGui import *
from file_manager import *
from table_gui import *
from server_connection import *
import about





# création de la vue et du conteneur
class TopWindow(QMainWindow):
	""" create a window being the main window of the gui """
	def __init__(self, core, params):
		# initiate the main widget
		QMainWindow.__init__(self)
		
		self.params = params
		self.platform = params.system
		self.debug = params.debug
		
		#core
		self.core = core

		# file manager
		self.fm = MyFileManager(self.platform)

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
		self.defineMenu()

		#######################"
		# central widget
		########################

		self.centralWidget = CentralWidget(fm, core, self, self.statusBar(), self.platform, self.debug)
		self.setCentralWidget(self.centralWidget)
		
		
		#pack the window
		self.setWindowTitle(TITLE_TOPWINDOW)

		self.show()
		
	def defineMenu(self):
		""" define menu of the application"""
		# exit button
		exitAction = QAction('&Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(qApp.quit)
		
		# remote server button
		remoteServer = QAction('&Remote server', self)
		remoteServer.setShortcut('Ctrl+R')
		remoteServer.setStatusTip('Deal with remote server')
		remoteServer.triggered.connect(self.launchRemoteServer)

		#about button
		aboutAction = QAction("&About " + PROG_SHORT_NAME, self)
		aboutAction.setStatusTip('About')
		self.connect(aboutAction, SIGNAL("triggered()"), self.launchAbout)
		
		# main menu bar
		self.menubar = self.menuBar()
		# fileMenu
		self.fileMenu = self.menubar.addMenu('&File')
		self.fileMenu.addAction(remoteServer)
		self.fileMenu.addAction(exitAction)
		
		#help menu
		self.helpMenu = self.menubar.addMenu("&?")
		self.helpMenu.addAction(aboutAction)
		
		
	def launchAbout(self):
		about.About(self)
		
	def launchRemoteServer(self):
		print("remote server")
		RemoteServerWindow(self.core.db, self.params, self.fm, self)
		
		
# ###########################################
#
#	Central widget
#
# ############################################


class CentralWidget(QWidget):
	""" a widget being the main widget within the topwindow"""
	""" this main widget will have all the required tabs and table within """
	def __init__(self, fm, core, parent, status, platform = PLATFORM_WINDOWS, debug = True):
		QWidget.__init__(self, parent)
		
		# operating system
		self.platform = platform
		
		# status bar
		self.status = status

		#init the central widget
		self.initCentralWidget(fm, core, debug)

	def initCentralWidget(self, fm, core, debug):
		#the top grid layout and tweak it


		self.grid = QGridLayout()
		self.grid.setSpacing(GRID_LAYOUT_SPACE)

		#SIDE PANEL
		self.sidePanel = SidePanel(fm, core, self, self.status, debug)
		
		#######################"
		# Place all the items
		########################

		

		# set the tabs
		self.tabsWidget = Tabs(core, self.sidePanel, self.status, self)
		self.grid.addWidget(self.tabsWidget, 1 , 0, 1, -1)


		# set the title
		self.title = QLabel(self)
		self.title.setText(TITLE_TOPWINDOW)
		self.grid.addWidget(self.title, 0 , 0, 1, -1)

		# set the side panel
		self.grid.addWidget(self.sidePanel, 2, 1)

		#setting the layout

		self.grid.setVerticalSpacing(1)
		self.setLayout(self.grid)










