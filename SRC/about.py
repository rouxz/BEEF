import static
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from table_gui import *

class About(QDialog):
	""" class displaying all information about the project """ 
	def __init__(self, *args):
		QDialog.__init__(self, *args)
		
		#window title
		self.setWindowTitle("About " + static.PROG_SHORT_NAME)
		
		self.layout = QVBoxLayout(self)
		
		self.layout.addWidget(QLabel(static.PROG_LONG_NAME))
		
		self.setLayout(self.layout)
		
		#display the dialog box
		self.show()