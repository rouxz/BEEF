from static import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from table_gui import *


class Window_modif(QDialog):
	""" windows to modif values with a tableView """
	
	def __init__(self, parent, CY, ref, month, type):
		QWidget.__init__(self, parent)
		
		
		#data used
		self.CY = CY
		self.ref = ref
		self.yoy = self.calcYoY(CY, ref)

		
		#set the UI
		self.initUI(month, type)
		
		#set to relative by default
		self.toRelative()
		
		#launch the UI
		self.exec_()
	
	
	def initUI(self, month, type):
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
		self.dataGroupBoxLayout.addWidget(QLabel(QString("CY"), self))
		self.CY_LE = QLineEdit(QString(str(self.CY)), self)
		self.dataGroupBoxLayout.addWidget(self.CY_LE)
		#ref
		self.dataGroupBoxLayout.addWidget(QLabel(QString("Ref"), self))
		self.ref_LE = QLineEdit(QString(str(self.ref)), self)
		self.dataGroupBoxLayout.addWidget(self.ref_LE)
		
		# YoY
		self.dataGroupBoxLayout.addWidget(QLabel(QString("YoY"), self))
		self.yoy_LE = QLineEdit(QString(str(self.yoy) + "%"), self)
		self.yoy_LE.setInputMask(QString("000.00%"))
		self.dataGroupBoxLayout.addWidget(self.yoy_LE)
		
		self.dataGroupBox.setLayout(self.dataGroupBoxLayout)
		
		# a group box for moving between cells and validating calculation
		self.moveGroupBox = QGroupBox(self)

		self.moveGroupBoxLayout = QHBoxLayout()
		
		self.buttonPrev = QPushButton(QString("<"), self)
		self.buttonValidate = QPushButton(QString("Validate"), self)
		self.buttonNext = QPushButton(QString(">"), self)
		
		self.moveGroupBoxLayout.addWidget(self.buttonPrev)
		self.moveGroupBoxLayout.addWidget(self.buttonValidate)
		self.moveGroupBoxLayout.addWidget(self.buttonNext)
		
		self.moveGroupBox.setLayout(self.moveGroupBoxLayout)
		
		#top label for displaying information
		self.topLabel = QLabel(QString(type + " - Month : " + str(month)))
		
		#adding the top label
		self.layout.addWidget(self.topLabel)
		
		#adding the groupbox of user action selection
		self.layout.addWidget(self.evolGroupBox)
		
		#adding the groupbox of user action selection
		self.layout.addWidget(self.dataGroupBox)
		
		#adding the groupbox of moving
		self.layout.addWidget(self.moveGroupBox)
		
		# connect slots and signals
		self.connect(self.yoy_LE, SIGNAL("editingFinished()"),self.updateCY)
		self.connect(self.yoy_LE, SIGNAL("returnPressed()"),self.updateCY)
		# void	editingFinished ()
# void	returnPressed ()
# void	selectionChanged ()
# void	textChanged ( const QString & text )
# void	textEdited ( co
		
		#setting the main layout
		self.setLayout(self.layout)
		
		self.setWindowTitle("Da Du Run")
		self.show()
		
	def calcYoY(self, CY, ref):
		if ref != 0:
			return (self.CY / self.ref - 1) * 100
		else:
			return 0
			
	def switchAbsoluteRelative(self, bool):
		""" define if the display should be set for relative evolution or absolute data """
		if bool == True:
			self.CY_LE.setReadOnly(True)
			self.ref_LE.setReadOnly(True)
		else:
			self.ref_LE.setReadOnly(True)
			self.yoy_LE.setReadOnly(True)
			
	def toAbsolute(self):
		""" set mode of input as absolute """
		self.switchAbsoluteRelative(False)
		
	def toRelative(self):
		""" set mode of input as relative """
		self.switchAbsoluteRelative(True)
		
		
	def recalculateCY(self, yoy):
		""" recalculate data for CY based on the reference and change the display """
		if self.ref !=0:
			#changing data
			self.CY = self.ref * (1 + yoy)
			print(self.CY)
			#changing display
			self.CY_LE.setText(str(self.CY))
		else:
			self.CY = 0
			
	def updateCY(self):
		""" change the display after having set a data in the YoY field """
		#odd behaviour on converting Qstring to float !!
		print("data entered " + str(self.yoy_LE.text().toUtf8()[:-1]).strip())
		#self.yoy = float(str(self.yoy_LE.text().toUtf8()[:-1]).strip())/100
		self.recalculateCY(float(str(self.yoy_LE.text().toUtf8()[:-1]).strip())/100)
		