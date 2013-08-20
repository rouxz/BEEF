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



	def importRemoteData(self, database):
		""" import all data from remote data to local db """
        #clear data within locale db
		#import all remote dataw
		pass

		
		
		
class RemoteServerWindow(QDialog):
	""" class for handling actions with remote server """
	def __init__(self, database, params, parent):
		QDialog.__init__(self, parent)
		
		self.debug = params.debug
		self.remote_server = RemoteServer(database, params)
		
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
		self.pull_widget_layout = QVBoxLayout()
		
		# title
		self.pull_title = QLabel("<b>Pull</b>")
		self.pull_widget_layout.addWidget(self.pull_title)
		
		self.pull_button = QPushButton("Retrieve all data")
		self.pull_widget_layout.addWidget(self.pull_button)
		
		self.pull_widget.setLayout(self.pull_widget_layout)
		
		
		
		self.layout.addWidget(self.pull_widget)
		
		# Push actions
		# ------------
		self.push_widget = QWidget(self)
		self.push_widget_layout = QGridLayout()
		
		# title
		self.push_title = QLabel("<b>Push</b>")
		self.push_widget_layout.addWidget(self.push_title, 0, 0, 1, -1)
		
		
		self.push_widget_layout.addWidget(QLabel("Select route perimeter"), 1, 0, 1, -1)
		
		self.push_button = QPushButton("Export my data")
		self.push_widget_layout.addWidget(self.push_button, 3, 0, 1, -1)
		
		# add the found hierarchy in the list
		self.listPerimeter = QListWidget(self.push_widget)
		self.push_widget_layout.addWidget(self.listPerimeter, 2, 0)
		
		#list data already sent
		self.pushed_data = QLabel("Pushed data")
		self.push_widget_layout.addWidget(self.pushed_data, 2, 1)
		
		self.push_widget.setLayout(self.push_widget_layout)
		
		self.layout.addWidget(self.push_widget)
		
		
		self.setLayout(self.layout)
		
		self.setWindowTitle("Remote connection")
		
		# behaviour of items
		self.connect(self.pull_button, SIGNAL("released()"), self.pullAction)
		self.connect(self.push_button, SIGNAL("released()"), self.pushAction)
		
	
	def definePerimeterList(self, fm):
		""" get the lists of files within the directory specified """
		# remove all if necessary
		self.listPerimeter.clear()
		# add the list
		for i in fm.getHierarchies():
			self.listPerimeter.addItem(QListWidgetItem(i, self.listPerimeter))
	
	
	
	def pullAction(self):
		if (self.debug):
			print("Pull actions")
		validate = QMessageBox.warning(self, "Validation required", "This actions will erase all changed already made on the local database\nAre you sure to proceed ?", QMessageBox.Cancel | QMessageBox.Ok)
		if validate == QMessageBox.Ok:
			if (self.debug):
				print("Pulling data")
			if (self.debug):
				print("Data pulled")
			
	
	def pushAction(self):
		if (self.debug):
			print("Push actions")
		validate = QMessageBox.warning(self, "Validation required", "This actions will erase every data already push towards remote the server\nAre you sure to proceed ?", QMessageBox.Cancel | QMessageBox.Ok)
		if validate == QMessageBox.Ok:
			if (self.debug):
				print("Pushing data")
			if (self.debug):
				print("Data pushed")
	
	
if __name__ == "__main__":
	p = DynamicParameters()
	
	app = QApplication(sys.argv)
	w = RemoteServerWindow(None, p, None)
	# topwindow of the gui
	w.showMaximized()
	sys.exit(app.exec_())