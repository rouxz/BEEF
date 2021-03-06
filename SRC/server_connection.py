﻿import static as STATIC
import os
import file_manager
from PyQt4.QtGui import *
from PyQt4.QtCore import *

try:
	from pyodbc import *
except ImportError:
	from sqlite3 import *

from param import *
from database import *


		
		
class RemoteServerWindow(QDialog):
	""" class for handling actions with remote server """
	def __init__(self, database, params, fm, parent):
		QDialog.__init__(self, parent)
		
		self.debug = params.debug
		self.params = params
		# self.user_profile is deprecated
		#self.user_profile = params.profile
		# self.remote_db = RemoteDatabase(params)
		self.remote_db = None
		self.file_manager = fm
		self.local_db = database
		
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
		self.pull_widget_layout.addWidget(QLabel("Fetch data from remote server"), 1, 0, 1, -1)
		
		self.pull_button = QPushButton("Retrieve data")
		self.pull_widget_layout.addWidget(self.pull_button, 3, 0)
	
		
		self.pull_ref_only_button = QPushButton("Retrieve ref data only")
		self.pull_widget_layout.addWidget(self.pull_ref_only_button, 3, 1)
		
		#progress bar
		self.pull_pbar = QProgressBar(self.pull_widget)
		self.pull_pbar.setMinimum(0)
		self.pull_pbar.setMaximum(100)
		self.pull_pbar.hide()
		self.pull_widget_layout.addWidget(self.pull_pbar, 2, 0, 1, -1)
		
		
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
		
		self.push_widget_layout.addWidget(QLabel("Select your profile"), 2, 0)
		self.push_widget_layout.addWidget(QLabel("Select route perimeter"), 2, 1)
		
		self.push_button = QPushButton("Export data")
		self.push_widget_layout.addWidget(self.push_button, 5, 0, 1, -1)
		
		# add profile information selection
		self.profile_widget = QWidget(self)
		self.profile_widget_layout = QVBoxLayout(self)
		self.IA_Button = QRadioButton("Inventory analyst", self.profile_widget)
		self.IM_Button = QRadioButton("Inventory team manager", self.profile_widget)
		self.ID_Button = QRadioButton("Inventory director", self.profile_widget)
		self.profile_widget_layout.addWidget(self.IA_Button)
		#by default select IA profile
		self.IA_Button.setChecked(True)
		self.profile_widget_layout.addWidget(self.IM_Button)
		self.profile_widget_layout.addWidget(self.ID_Button)
		self.profile_widget.setLayout(self.profile_widget_layout)
		
		self.push_widget_layout.addWidget(self.profile_widget, 3, 0)
		
		# add the found hierarchy in the list
		self.listPerimeter = QListWidget(self.push_widget)
		self.defineListPerimeter()
		self.listPerimeter.setSelectionMode(QAbstractItemView.SingleSelection)
		self.listPerimeter.setCurrentRow(0)
		self.push_widget_layout.addWidget(self.listPerimeter, 3, 1)
		
		#list data already sent
		self.pushed_data = QLabel("Pushed data")
		self.push_widget_layout.addWidget(self.pushed_data, 3, 2)
		
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
		self.connect(self.pull_ref_only_button, SIGNAL("released()"), self.pullRefOnlyAction)
		self.connect(self.push_button, SIGNAL("released()"), self.pushAction)
		
	
	def defineListPerimeter(self):
		""" get the lists of files within the directory specified """
		# remove all if necessary
		self.listPerimeter.clear()
		# add the list
		for i in self.file_manager.getHierarchies():
			self.listPerimeter.addItem(QListWidgetItem(i, self.listPerimeter))
	
	
	def pullActionParam(self, tables, step, validationMessage):
		if (self.debug):
			print("Pull actions")
		validate = QMessageBox.warning(self, "Validation required", validationMessage, QMessageBox.Cancel | QMessageBox.Ok)
		
		if validate == QMessageBox.Ok:
		
			#connection to remote_db
			self.remote_db = RemoteDatabase(self.params)
			
			#start progress bag
			self.pull_pbar.show()
			self.pull_pbar.setValue(0)
			
			# table_to_copy = ("DATA_RAW", "DATA_REF_0", "DATA_REF_1", "DATA_REF_2", "DATA_REF_3", "RFS_RETRAITEMENT", "TABLE_REF")
			table_to_copy = tables
			# table_to_copy = ("TABLE_REF", "DATA_RAW")
			
			if (self.debug):
				print("Pulling data")
				
			# clear local database
			self.local_db.clearTableList(tables)
			
			# import data
			for table in table_to_copy:
				self.local_db.copyTable(table, self.remote_db)
				self.pull_pbar.setValue(self.pull_pbar.value() + step)
			
			if (self.debug):
				print("Data pulled")
			#finish progress bag
			self.pull_pbar.setValue(100)
			
			#closing connection
			self.remote_db.__del__()
	
	def pullRefOnlyAction(self):
		self.pullActionParam(("DATA_REF_0", "DATA_REF_1", "DATA_REF_2", "DATA_REF_3", "RFS_RETRAITEMENT", "TABLE_REF"),12, "This action will erase all references in the local database\nAre you sure to proceed ?")
	
	
	def pullAction(self):
		self.pullActionParam(("DATA_RAW", "DATA_REF_0", "DATA_REF_1", "DATA_REF_2", "DATA_REF_3", "RFS_RETRAITEMENT", "TABLE_REF"),12, "This action will erase all changed already made on the local database\nAre you sure to proceed ?")
	
	def pushAction(self):
		if (self.debug):
			print("Push actions")
			
		profile = self.findProfile()
		validate = QMessageBox.warning(self, "Validation required", "This actions will erase every data already pushed towards remote the server\n" + \
								"Your profile is " + profile + "\nAre you sure to proceed ?", QMessageBox.Cancel | QMessageBox.Ok)
		
		
		
		if validate == QMessageBox.Ok:
		
			# connection to remote db
			self.remote_db = RemoteDatabase(self.params)
			
			# look for list of lines 
			file2read = str(self.listPerimeter.currentItem().text().toUtf8())
			lstLines = self.file_manager.getSublines(file2read)
			if (self.debug):
				print("Following routes will be impacted:")
				for line in lstLines:
					print("- " + line) 
				
				
			# send data
			try:
				# table_destination = STATIC.DICT_PROFILE[self.user_profile]
				table_destination = STATIC.DICT_PROFILE[profile]
				if (self.debug):
					print("Pushing data to " + table_destination)
				# init progress bar
				self.push_pbar.show()
				self.push_pbar.setValue(0)
				if (self.debug):
					print("Pushing data")
					
					self.local_db.sendDataToExternal(lstLines, table_destination, self.remote_db) 
					
				if (self.debug):
					print("Data pushed")
				#finish progress bag
				self.push_pbar.setValue(100)
				
				#closing connection
				self.remote_db.__del__()
				
			except:
				print("Error in the user profile - please check " + STATIC.PARAM_FILE)
				QMessageBox.critical(self,"Error", "Error in the user profile - please check " + STATIC.PARAM_FILE,  QMessageBox.Ok)
			
			
	def findProfile(self):
		""" find the profile already selected in the gui """
		if (self.IA_Button.isChecked()):
			profile = "IA"
		elif (self.IM_Button.isChecked()):
			profile = "IM"
		else:
			profile = "ID"
		
		if (self.debug):
			"Your profile is " + profile
		return profile
	
if __name__ == "__main__":
	p = DynamicParameters()
	
	app = QApplication(sys.argv)
	w = RemoteServerWindow(None, p, None, None)
	# topwindow of the gui
	w.showMaximized()
	sys.exit(app.exec_())