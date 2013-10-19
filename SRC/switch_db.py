import static as STATIC
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


		
		
class SwitchDB(QDialog):
	""" class for switching working database """
	def __init__(self, database, params, fm, parent):
		QDialog.__init__(self, parent)
		
		self.params = params
		self.debug = params.debug
		self.file_manager = fm
	
		#connection to local db
		self.database = database
		self.dbname = database.dbname
	
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
	
	
		
		# title
		self.title = QLabel("<b>Switching database</b>")
		self.layout.addWidget(self.title)
		
		#line edit with database name
		self.database_le = QLineEdit(self)
		self.database_le.setText(self.database.dbname)
		self.layout.addWidget(self.database_le)
		
		self.button_filechooser = QPushButton("Choose other db")
		self.button_ok =  QPushButton("OK")
		self.layout.addWidget(self.button_filechooser)
		self.layout.addWidget(self.button_ok)
		
		
		# settting the layout
		self.setLayout(self.layout)
		
		# behaviour of items
		self.connect(self.button_filechooser, SIGNAL("released()"), self.chooseDb)
		self.connect(self.button_ok, SIGNAL("released()"), self.changeConnectionDb)
		
		
	
	def chooseDb(self):
		""" choose another database in QFileDialog """
		if self.params.system != "linux2":
			#connection MS ACCESS
			path = STATIC.DATA_DIR
		else:
			# Connection to sqlite3
			path = STATIC.DBPATH_UNIX 
				
		# fetch the database name
		self.database_le.setText(QFileInfo(QFileDialog.getOpenFileName(self, 'Open file', path,  "databases (*.accdb *.db)")).fileName())
        
	def changeConnectionDb(self):
		#change connection
		self.database.disconnect()
		self.database.connect(str(self.database_le.text()))
		# hide window
		self.hide()
	
if __name__ == "__main__":
	p = DynamicParameters()
	
	app = QApplication(sys.argv)
	w = SwitchDB(LocalDatabase(p), p, None, None)
	# topwindow of the gui
	w.showMaximized()
	sys.exit(app.exec_())