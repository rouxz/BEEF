from static import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from table_gui import *


class Window_modif(QDialog):
	""" windows to modif values with a tableView """
	
	def __init__(self, parent, CY, ref):
		QWidget.__init__(self, parent)
		
		
		#data used
		self.CY = CY
		self.ref = ref
		self.yoy = self.calcYoY(CY, ref)
		
		#moving to another data
		
		
		self.initUI()
		self.exec_()
	
	
	def initUI(self):
		""" display the window properly """
		
		#global layout for the widget
		self.layout = QVBoxLayout()
		
		# a group box for selecting how we want to proceed (relative evolution or absolute value)
		self.evolGroupBox = QGroupBox(self)
		self.evolGroupBox.setTitle(QString("Choose type of modification"))
		
		self.evolGroupBoxLayout = QVBoxLayout()
		self.evolGroupBoxLayout.addWidget(QRadioButton(QString("Absolute"), self))
		self.evolGroupBoxLayout.addWidget(QRadioButton(QString("Relative evolution"), self))
		
		self.evolGroupBox.setLayout(self.evolGroupBoxLayout)
		
		# a group box for defining the data
		self.dataGroupBox = QGroupBox(self)
		self.dataGroupBox.setTitle(QString("Data"))
		
		self.dataGroupBoxLayout = QVBoxLayout()
		#CY
		self.dataGroupBoxLayout.addWidget(QTextEdit(QString(str(self.CY)), self))
		#PY
		self.dataGroupBoxLayout.addWidget(QTextEdit(QString(str(self.ref)), self))
		# YoY
		self.dataGroupBoxLayout.addWidget(QTextEdit(QString(str(self.yoy)), self))
		
		self.dataGroupBox.setLayout(self.dataGroupBoxLayout)
		
		# a group box for moving between cells
		self.moveGroupBox = QGroupBox(self)

		self.moveGroupBoxLayout = QVBoxLayout()
		self.moveGroupBoxLayout.addWidget(QLabel(QString("Absolute"), self))
		
		self.moveGroupBox.setLayout(self.moveGroupBoxLayout)
		
		
		#adding the groupbox of user action selection
		self.layout.addWidget(self.evolGroupBox)
		
		#adding the groupbox of user action selection
		self.layout.addWidget(self.dataGroupBox)
		
		#adding the groupbox of moving
		self.layout.addWidget(self.moveGroupBox)
		
		self.setLayout(self.layout)
		
		self.setWindowTitle("Da Du Run")
		self.show()
		
	def calcYoY(self, CY, ref):
		if ref != 0:
			return self.CY / self.ref - 1
		else:
			return 0