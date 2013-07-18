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
		
		# general information about programme
		self.layout.addWidget(QLabel(static.PROG_LONG_NAME))
		self.layout.addWidget(QLabel(str(static.VERSION)))
		
		self.layout.addWidget(QLabel(static.EXPLANATIONS))
		
		# license
		self.layout.addWidget(QLabel(static.LICENSE_WORDING))
		self.layout.addWidget(QLabel(static.LICENSE))
		
		#technologies used
		self.layout.addWidget(QLabel(static.TECHNOLOGY_HEADER))
		for tech in static.TECHNOLOGIES_LIST:
			self.layout.addWidget(QLabel(tech))
		
		
		self.setLayout(self.layout)
		
		#display the dialog box
		self.show()