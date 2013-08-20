import static as STATIC
import os
import file_manager
from PyQt4.QtGui import *
from PyQt4.QtCore import *

try:
	from pyodbc import *
except ImportError:
	from sqlite3 import *

# retirer
from param import *

class RemoteServer():

	def __init__(self, database, params):
		""" connect local database to remote one """
		self.debug = params.debug
		self.platform = params.system

		try:

			#get address of database
			self.remote_db = params.remote_db_address

			if self.platform == STATIC.PLATFORM_WINDOWS:
				#connection MS ACCESS
				print("Connecting to : " + self.remote_db)
				self.cnx = connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=" +  self.remote_db.replace("\\", "\\\\") + ";Uid=Admin;Pwd=;")
			else:
				# Connection to sqlite3
				print("Platform different than windows / no remote connection")
				return -1

			print("Connection to remote db " + self.remote_db + " successfull")

		except:
			print("Connection to db " + self.remote_db + " failed")



	def importRemoteData(self):
		""" import all data from remote data to local db """
        #clear data within locale db
		#import all remote dataw
		pass

	def sendLocalData(self):
		""" send data from local data to remote database """
		pass
		
		
		
class RemoteServerWindow(QDialog):
	""" class for handling actions with remote server """
	def __init__(self, database, params, fm, parent):
		QDialog.__init__(self, parent)
		
		self.debug = params.debug
		self.remote_server = RemoteServer(database, params)
		self.file_manager = fm
		
		#set the UI
		self.initUI()
		
		#set to relative by default
		# self.toRelative(True)
		
		#launch the UI
		self.exec_()
	
	def initUI(self):
		if (self.debug):
			print("defining UI")
		
		self.layout = QVBoxLayout()
		
		# Pull actions
		# ------------
		self.pull_widget = QWidget(self)
		self.pull_widget_layout = QGridLayout()
		
		# title
		self.pull_title = QLabel("<b>Pull</b>")
		self.pull_widget_layout.addWidget(self.pull_title, 0, 0, 1, -1)
		self.pull_widget_layout.addWidget(QLabel("Fetch all data from remote server"), 1, 0, 1, -1)
		
		self.pull_button = QPushButton("Retrieve data")
		self.pull_widget_layout.addWidget(self.pull_button, 3, 0, 1, -1)
		
		#progress bar
		self.pull_pbar = QProgressBar(self.pull_widget)
		self.pull_pbar.setMinimum(0)
		self.pull_pbar.setMaximum(100)
		self.pull_pbar.hide()
		self.pull_widget_layout.addWidget(self.pull_pbar, 2, 0)
		
		
		self.pull_widget.setLayout(self.pull_widget_layout)
		
		
		
		self.layout.addWidget(self.pull_widget)
		
		# Push actions
		# ------------
		self.push_widget = QWidget(self)
		self.push_widget_layout = QGridLayout()
		
		# title
		self.push_title = QLabel("<b>Push</b>")
		self.push_widget_layout.addWidget(self.push_title, 0, 0, 1, -1)
		self.push_widget_layout.addWidget(QLabel("Send data to remote server"), 1, 0, 1, -1)
		
		self.push_widget_layout.addWidget(QLabel("Select route perimeter"), 2, 0, 1, -1)
		
		self.push_button = QPushButton("Export data")
		self.push_widget_layout.addWidget(self.push_button, 5, 0, 1, -1)
		
		# add the found hierarchy in the list
		self.listPerimeter = QListWidget(self.push_widget)
		self.defineListPerimeter()
		self.listPerimeter.setSelectionMode(QAbstractItemView.SingleSelection)
		self.push_widget_layout.addWidget(self.listPerimeter, 3, 0)
		
		#list data already sent
		self.pushed_data = QLabel("Pushed data")
		self.push_widget_layout.addWidget(self.pushed_data, 3, 1)
		
		# progress bar
		self.push_pbar = QProgressBar(self.push_widget)
		self.push_pbar.setMinimum(0)
		self.push_pbar.setMaximum(100)
		self.push_pbar.hide()
		self.push_widget_layout.addWidget(self.push_pbar, 4, 0)
		
		self.push_widget.setLayout(self.push_widget_layout)
		
		self.layout.addWidget(self.push_widget)
		
		
		self.setLayout(self.layout)
		
		self.setWindowTitle("Remote connection")
		
		# behaviour of items
		self.connect(self.pull_button, SIGNAL("released()"), self.pullAction)
		self.connect(self.push_button, SIGNAL("released()"), self.pushAction)
		
	
	def defineListPerimeter(self):
		""" get the lists of files within the directory specified """
		# remove all if necessary
		self.listPerimeter.clear()
		# add the list
		for i in self.file_manager.getHierarchies():
			self.listPerimeter.addItem(QListWidgetItem(i, self.listPerimeter))
	
	
	
	def pullAction(self):
		if (self.debug):
			print("Pull actions")
		validate = QMessageBox.warning(self, "Validation required", "This actions will erase all changed already made on the local database\nAre you sure to proceed ?", QMessageBox.Cancel | QMessageBox.Ok)
		if validate == QMessageBox.Ok:
			#start progress bag
			self.pull_pbar.show()
			self.pull_pbar.setValue(0)
			if (self.debug):
				print("Pulling data")
			
			# import data
			self.remote_server.importRemoteData()
			
			if (self.debug):
				print("Data pulled")
			#finish progress bag
			self.pull_pbar.setValue(100)
	
	def pushAction(self):
		if (self.debug):
			print("Push actions")
		validate = QMessageBox.warning(self, "Validation required", "This actions will erase every data already push towards remote the server\nAre you sure to proceed ?", QMessageBox.Cancel | QMessageBox.Ok)
		if validate == QMessageBox.Ok:
			# init progress bar
			self.push_pbar.show()
			self.push_pbar.setValue(0)
			if (self.debug):
				print("Pushing data")
				
			# send data
			self.remote_server.sendLocalData()
			
			if (self.debug):
				print("Data pushed")
			#finish progress bag
			self.push_pbar.setValue(100)
	
if __name__ == "__main__":
	p = DynamicParameters()
	
	app = QApplication(sys.argv)
	w = RemoteServerWindow(None, p, None, None)
	# topwindow of the gui
	w.showMaximized()
	sys.exit(app.exec_())