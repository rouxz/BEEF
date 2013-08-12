from static import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from table_gui import *
import re
import event

class Window_modif(QDialog):
	""" windows to modif values with a tableView """
	
	def __init__(self, parent, index, debug = True):
		QWidget.__init__(self, parent)
		
		self.debug = debug
		
		#parent - MyTableView
		self.parentTable = parent
		
		# number of routes on which the evolution will be applied
		self.numberOfRoutes = self.parentTable.core.numberOfRoutes
		
		#initiate data
		self.initData(index)
		
		#side panel to send the events
		self.sidePanel = self.parentTable.sidePanel

		
		
		#set the UI
		self.initUI()
		
		#set to relative by default
		self.toRelative(True)
		
		#launch the UI
		self.exec_()
	
	
	def initData(self, index):
		# index QModelIndex representing the cell launching this pop up
		self.index = index
		
		#line from where the pop up has been called
		self.header = VERTICAL_HEADER[index.row()]
		
		# define the index for CY, Ref and YoY
		self.defineIndexes(index)
		
		# flag to know if an action has been sent to the gui
		self.actionSent = 0
		
		#flag for modification tracking
		self.modifFlag = False
		
		#data used
		self.getData()
		
		#set the first yoy
		self.yoy = self.calcyoY(self.cy, self.ref)

	
	def initUI(self):
		""" display the window properly """
		
		#global layout for the widget
		self.layout = QVBoxLayout()
		
		
		
		# if the numberOfRoutes handled is superior to 1, you cannot feed absolute data !
		
		
		if  self.numberOfRoutes <= 1:
			
			# a group box for selecting how we want to proceed (relative evolution or absolute value)
			self.evolGroupBox = QGroupBox(self)
			self.evolGroupBox.setTitle(QString("Choose type of modification"))
		
			self.evolGroupBoxLayout = QVBoxLayout()
			self.radioButtonAbsolute = QRadioButton(QString("Absolute"), self)
			self.evolGroupBoxLayout.addWidget(self.radioButtonAbsolute)
		
			self.radioButtonRelative = QRadioButton(QString("Relative evolution"), self)
			self.evolGroupBoxLayout.addWidget(self.radioButtonRelative)
			
			self.evolGroupBox.setLayout(self.evolGroupBoxLayout)
		
		# a group box for defining the data
		self.dataGroupBox = QGroupBox(self)
		self.dataGroupBox.setTitle(QString("Data"))
		
		self.dataGroupBoxLayout = QVBoxLayout()
		#cy
		self.dataGroupBoxLayout.addWidget(QLabel(QString("cy (000)"), self))
		self.cy_LE = QLineEdit(self.convertFloatToString(self.cy), self)
		self.dataGroupBoxLayout.addWidget(self.cy_LE)
		#ref
		self.dataGroupBoxLayout.addWidget(QLabel(QString("Ref (000)"), self))
		self.ref_LE = QLineEdit(self.convertFloatToString(self.ref), self)
		self.dataGroupBoxLayout.addWidget(self.ref_LE)
		
		# YoY
		self.dataGroupBoxLayout.addWidget(QLabel(QString("YoY"), self))
		self.yoy_LE = QDoubleSpinBox(self)
		# parameters for Spinbox
		self.yoy_LE.setSuffix(" %")
		self.yoy_LE.setRange(-100,99999)
		self.yoy_LE.setDecimals(2)
		
		#setting value of spinbox
		self.yoy_LE.setValue(self.yoy)
		
		# self.yoy_LE.replace(QLatin1Char('.'), QLocale().decimalPoint()))
		# self.yoy_LE.replace(QLocale().decimalPoint(), QUnicodeChar('.'))
		
		# self.yoy_LE = QLineEdit(QString(str(self.yoy)), self)
		
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
		self.topLabel = QLabel(QString(self.header[:-3] + " - Month : " + str(self.index.column()+1)))
		
		#adding the top label
		self.layout.addWidget(self.topLabel)
		
		#adding the groupbox of user action selection
		if self.numberOfRoutes <= 1:
			self.layout.addWidget(self.evolGroupBox)
		
		#adding the groupbox of data
		self.layout.addWidget(self.dataGroupBox)
		
		#adding the groupbox of moving
		self.layout.addWidget(self.moveGroupBox)
		
		# connect slots and signals
		# self.connect(self.yoy_LE, SIGNAL("editingFinished()"),self.update_cy)
		# self.connect(self.yoy_LE, SIGNAL("returnPressed()"),self.update_cy)
		self.connect(self.yoy_LE, SIGNAL("valueChanged(double)"),self.update_cy)
		self.connect(self.buttonValidate, SIGNAL("released()"), self.validateAndClose)
		
		# for switching between absolute and relative
		if self.numberOfRoutes <= 1:
			self.connect(self.radioButtonAbsolute, SIGNAL("toggled(bool)"),self.toAbsolute)
			self.connect(self.radioButtonRelative, SIGNAL("toggled(bool)"),self.toRelative)
			#Updating CY for absolute
			self.connect(self.cy_LE, SIGNAL("editingFinished()"), self.callbackModifCY)
			
		
		# void	editingFinished ()

		
		#setting the main layout
		self.setLayout(self.layout)
		
		self.setWindowTitle(self.header)
		self.show()
	
	
	def convertFloatToString(self, flt):
		# return QString("%L1").arg(round(float(flt)/1000,1))
		return QString("%L1").arg(round(flt/1000,1))
	
	
	def defineIndexes(self, index):
		""" define the index for the CY, ref and YoY cells in the tableView """ 
		
		
		if self.header[-3:].strip() == "CY":
			self.cyIndex = index
			self.refIndex = index.sibling(index.row()+1, index.column())
			self.YoYIndex = index.sibling(index.row()+2, index.column())
		elif self.header[-3:].strip() == "Ref":
			self.cyIndex = index.sibling(index.row()-1, index.column())
			self.refIndex = index
			self.YoYIndex = index.sibling(index.row()+1, index.column())
		else:
			self.cyIndex = index.sibling(index.row()-2, index.column())
			self.refIndex = index.sibling(index.row()-1, index.column())
			self.YoYIndex = index
	
	
	def getData(self):
		""" retrieve cy and ref data """
		# self.cy = self.cyIndex.data(Qt.DisplayRole).toPyObject()
		# self.ref = self.refIndex.data(Qt.DisplayRole).toPyObject()
		self.cy = self.parentTable.tableModel.getDataFloat(self.cyIndex.row(),self.cyIndex.column())
		self.ref = self.parentTable.tableModel.getDataFloat(self.refIndex.row(),self.refIndex.column())
		
		#print("Popup " + str(self.cy)  + "-" + str(self.ref))

	
	def calcyoY(self, cy, ref):
		""" define yoy data """
		if ref != 0:
			return (self.cy / self.ref - 1) * 100
		else:
			return 0
			
	def switchAbsoluteRelative(self, bool):
		""" define if the display should be set for relative evolution or absolute data """
		
		if bool == True:
			# allow proper text edit to be editable or not
			self.cy_LE.setReadOnly(True)
			self.ref_LE.setReadOnly(True)
			self.yoy_LE.setReadOnly(False)
			# check the right radiobutton
			if self.numberOfRoutes <= 1:
				self.radioButtonRelative.setChecked(True)
			if self.debug == True:
				print("Going to relative")
		else:
			self.ref_LE.setReadOnly(True)
			self.yoy_LE.setReadOnly(True)
			self.cy_LE.setReadOnly(False)
			if self.numberOfRoutes <= 1:
				self.radioButtonAbsolute.setChecked(True)
			if self.debug == True:
				print("Going to absolute")
			
	def toAbsolute(self, checked):
		""" set mode of input as absolute """
		if (checked):
			self.switchAbsoluteRelative(False)
		
	def toRelative(self, checked):
		""" set mode of input as relative """
		if (checked):
			self.switchAbsoluteRelative(True)
		
		
	def recalculate_cy(self, yoy):
		""" recalculate data for cy based on the reference and change the display """
		if self.ref !=0:
			#changing data
			self.cy = self.ref * (1 + yoy)
			#print(self.cy)
			#Update the modif flag if the yoy is different than the previous one
			if self.yoy != yoy:
				self.modifFlag = True
			
			#changing display
			self.cy_LE.setText(self.convertFloatToString(self.cy))
		else:
			self.cy = 0
			
	def update_cy(self):
		""" change the display after having set a data in the YoY field """
		self.recalculate_cy((self.yoy_LE.value())/100)
		# print((self.yoy_LE.value())/100)
		
		
	def callbackModifCY(self):
		""" callback function launched once self.cy_LE has been modified """
		# for debuggin purpose
		if self.debug == True:
			print("Callback on cy modification")
		
		# update data model in the system
		tmp = self.cy_LE.text().toFloat()
		if (tmp[1] == True) and (tmp[0]>=0):
			self.cy = tmp[0] * 1000
		else:
			self.cy_LE.setText(self.convertFloatToString(self.cy))
		
		
		
		# tell the class something has been modified
		self.modifFlag = True
		
		# update the YoY
		self.yoy_LE.setValue(self.calcyoY(self.cy, self.ref))
		
	
		
		
	def validate(self):
		""" send the data to the tableview and the required action to the gui """
		
		if self.actionSent == 0 and self.modifFlag == True:
			
			# find the contribution 
			if  self.header[:3] == "RPK":
					yld  =  self.header[3:7].strip()
			elif self.header[:5] == "Yield":
					yld = self.header[5:9].strip()

			# get previous data in the table
			val_rev_init = self.parentTable.tableModel.getDataFloat(VERTICAL_HEADER.index("Rev " + yld + " CY"), self.index.column())
			val_RPK_init = self.parentTable.tableModel.getDataFloat(VERTICAL_HEADER.index("RPK " + yld + " CY"), self.index.column())
					
			#modify revenue accordingly
			# RPK change revenue with constant yield
			if self.header[:3] == "RPK":
				valRPK = self.cy
				valRev = self.parentTable.tableModel.getDataFloat(VERTICAL_HEADER.index("Yield " + yld + " CY"), self.index.column()) * self.cy
				self.parentTable.tableModel.setData(self.index.sibling(VERTICAL_HEADER.index("Rev " + yld + " CY"), self.index.column()), valRev, Qt.DisplayRole)
			# Yield change revenue with constant RPK
			elif self.header[:5] == "Yield":
				# current RPK
				valRPK = self.parentTable.tableModel.getDataFloat(VERTICAL_HEADER.index("RPK " + yld + " CY"), self.index.column())
				# new revenue
				valRev = valRPK * self.cy
				self.parentTable.tableModel.setData(self.index.sibling(VERTICAL_HEADER.index("Rev " + yld + " CY"), self.index.column()), valRev, Qt.DisplayRole)
			
			
			#modify the value according to what has been put in
			self.parentTable.tableModel.setData(self.cyIndex, self.cy, Qt.DisplayRole)
			self.parentTable.tableModel.setData(self.YoYIndex, self.yoy_LE.text(), Qt.DisplayRole)
			
			#update totals
			self.parentTable.setDataConsistency()
			
			#update the gui
			self.parentTable.updateDisplay()
			
			#create a modif event
			
			#for yoy modification.
		
			if (self.numberOfRoutes <= 1 and self.radioButtonRelative.isChecked()) or self.numberOfRoutes > 1:
			
					e = event.EventModifValue(valRev / val_rev_init, valRPK / val_RPK_init, self.index.column()+1, yld, self.parentTable.flow )

			
			else:
				#absolute modification
				e = event.EventAddAbsoluteData(valRev, valRPK, self.index.column()+1, yld, self.parentTable.flow, self.debug)
				
				if self.debug == True:
					print("Value sent to the action handler is : " + str(self.cy))
			
			
			
			
			
			
			# add event if not null
			if e != None:
				self.sidePanel.user_interaction.addPendingActions(e)
				self.actionSent = 1
			
		
	def validateAndClose(self):
		self.validate()
		#close the window
		self.done(0)
					
		