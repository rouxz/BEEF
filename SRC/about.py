from static import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from table_gui import *

class About(QDialog):
	""" class displaying all information about the project """ 
	def __init__(self, *args):
		QDialog.__init__(self, *args)