from static import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from table_gui import *
import re
import event

class Window_modif(QDialog):
	""" windows to modif values with a tableView """
	
	
	def __init__(self, parent, index, debug = True):
		QDialog.__init__(self, parent)
		
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
		
		# list of events
		self.eventList = []
		for r in xrange(12):
			self.eventList.append([])
		
		#set to relative by default
		self.toRelative(True)
		
		#launch the UI
		self.exec_()
			
	
	
	
	# #####################
	#		 DATA
	# #####################
	
	def initData(self, index):
		# print("entre dans fonction initData")
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
		print("self.modifFlag = False dans initData")
		
		#data used
		self.getData()
		
		#set the first yoy
		self.yoy = self.calcyoY(self.cy, self.ref)
		# print("Initialization of self.yoy = " + str(self.yoy))

	def defineIndexes(self, index):
		# print("entre dans fonction defineIndexes")
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
		# print("entre dans fonction getData")
		""" retrieve cy and ref data """

		self.cy = self.parentTable.tableModel.getDataFloat(self.cyIndex.row(),self.cyIndex.column())
		self.ref = self.parentTable.tableModel.getDataFloat(self.refIndex.row(),self.refIndex.column())


	
	def calcyoY(self, cy, ref):
		# print("entre dans fonction calcyoY")
		""" define yoy data """
		if ref != 0:
			return (self.cy / self.ref - 1) * 100
		else:
			return 100
		
		
		
		
		
	# #####################
	#		 DISPLAY
	# #####################	
		
	
	def initUI(self):
		# print("entre dans fonction initUI")
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
		
		# label for CY data
		if self.header[:5] == "Yield":
			#cy
			self.dataGroupBoxLayout.addWidget(QLabel(QString(LABEL_CY_Yield), self))
		else:
			self.dataGroupBoxLayout.addWidget(QLabel(QString(LABEL_CY_RPK), self))

		
		#Line edit for displaying CY
		self.cy_LE = QLineEdit(self.convertFloatToString(self.cy), self)
		self.dataGroupBoxLayout.addWidget(self.cy_LE)
		
		
		# label for reference data
		if self.header[:5] == "Yield":
			#cy
			self.dataGroupBoxLayout.addWidget(QLabel(QString(LABEL_REF_Yield), self))
		else:
			self.dataGroupBoxLayout.addWidget(QLabel(QString(LABEL_REF_RPK), self))

		
		#Line edit for displaying Reference data
		self.ref_LE = QLineEdit(self.convertFloatToString(self.ref), self)
		self.dataGroupBoxLayout.addWidget(self.ref_LE)
		
		# Index
		self.dataGroupBoxLayout.addWidget(QLabel(QString("Index"), self))
		self.yoy_LE = QDoubleSpinBox(self)
		# parameters for Spinbox
		self.yoy_LE.setSuffix(" %")
		self.yoy_LE.setRange(-100,99999)
		self.yoy_LE.setDecimals(2)
		
		#setting value of spinbox
		self.yoy_LE.setValue(self.yoy)
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
		self.topLabel = QLabel(self.topLabelValue())
		
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
		#--------------------------------
		# self.connect(self.yoy_LE, SIGNAL("editingFinished()"),self.update_cy)
		# self.connect(self.yoy_LE, SIGNAL("returnPressed()"),self.update_cy)
		self.connect(self.yoy_LE, SIGNAL("valueChanged(double)"),self.update_cy)
		self.connect(self.buttonValidate, SIGNAL("released()"), self.validateAndClose)
		self.connect(self, SIGNAL('triggered()'), self.closeEvent)
		
		# for switching between absolute and relative
		if self.numberOfRoutes <= 1:
			self.connect(self.radioButtonAbsolute, SIGNAL("toggled(bool)"),self.toAbsolute)
			self.connect(self.radioButtonRelative, SIGNAL("toggled(bool)"),self.toRelative)
			#Updating CY for absolute
			# self.connect(self.cy_LE, SIGNAL("editingFinished()"), self.callbackModifCY)
			self.connect(self.cy_LE, SIGNAL("textEdited(const QString&)"), self.callbackModifCY)
			
		# for going to the left or the right
		self.connect(self.buttonNext, SIGNAL("released()"), self.moveToRight)
		self.connect(self.buttonPrev, SIGNAL("released()"), self.moveToLeft)
		
		#setting the main layout
		self.setLayout(self.layout)
		
		self.setWindowTitle(self.header)
		self.show()
 
	def closeEvent(self, event):
		# print "Closing modifWindow and saving changes"
		self.validateAndClose()
	
	def topLabelValue(self):
		# print("entre dans fonction topLabelValue")
		""" define the label on top of the window indicating what data are we dealing with"""
		return QString(self.header[:-3] + " - Month : " + str(self.index.column()+1))
	
	
	def convertFloatToString(self, flt):
		""" function used to properly display figures in the line edits """

		if self.header[:5] == "Yield":
			return QString("%L1").arg(round(flt*100,3))
		else:
			return QString("%L1").arg(round(flt/1000,1))
	
	def updateDisplay(self):
		# print("entre dans fonction updateDisplay")
		""" update the display with the current data enclosed in the object """
		
		#update the header
		self.topLabel.setText(self.topLabelValue())
		
		#update CY
		self.cy_LE.setText(self.convertFloatToString(self.cy))
		
		#update REF
		self.ref_LE.setText(self.convertFloatToString(self.ref))
		
		#update the index
		self.yoy_LE.setValue(self.calcyoY(self.cy, self.ref))
	
	
	
	
	

	# #####################
	#		 BEHAVIOUR
	# #####################	
	

	
	def switchAbsoluteRelative(self, bool):
		# print("entre dans fonction switchAbsoluteRelative")
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
		print("entre dans fonction recalculate_cy")
		""" recalculate data for cy based on the reference and change the display in the pop up window """
		if self.ref !=0:
			#changing data
			self.cy = self.ref * (1 + yoy)
			temp = abs(round(self.yoy/100,4) - yoy)
			# print("temp = " + str(temp))
			
			#Update the modif flag if the yoy is different than the previous one
			if (temp >= 0.001):
				self.modifFlag = True
				print("self.modifFlag = True dans recalculate yoy car different du precedent")
			
			#changing display
			self.cy_LE.setText(self.convertFloatToString(self.cy))
		else:
			self.cy = 0
			
	def update_cy(self):
		""" change the display after having set a data in the YoY field """
		
		if self.cy_LE.isReadOnly() == True:
			self.recalculate_cy((self.yoy_LE.value())/100)
		
	
	def update_gui(self):
		# print("entre dans fonction update_gui")
		""" send the data to the tableview and the required action to the gui """
		print("self.actionSent = " + str(self.actionSent) + "   self.modifFlag = " + str(self.modifFlag))
		
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
				print("------------ valRPK = " + str(valRPK))
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
			self.parentTable.parent.consistencyAllFlows()
			self.parentTable.updateDisplay()
						
			self.createEvent(valRev, val_rev_init, valRPK, val_RPK_init, yld)
			
	
	def createEvent(self, valRev, val_rev_init, valRPK, val_RPK_init, yld):
	#create a modif event
		
		print("create event for month " + str(self.index.column()+1))
		#for yoy modification	

		e_old = self.eventList[self.index.column()]
		FlagAbsolute = 0
		if e_old != [] and e_old.type == ABSOLUTE:
			FlagAbsolute = 1
		
		if self.numberOfRoutes > 1 or (self.numberOfRoutes <= 1 and self.radioButtonRelative.isChecked() and FlagAbsolute == 0):
			
			IdxRPK = valRPK / val_RPK_init
			IdxRev = valRev / val_rev_init
			
			if  e_old != [] and e_old.type == MODIFICATION:
					IdxRPK = e_old.indexRPK * IdxRPK
					IdxRev = e_old.indexRev * IdxRev
		
			e = event.EventModifValue(IdxRev, IdxRPK, self.index.column()+1, yld, self.parentTable.flow )
			self.eventList[self.index.column()] = e				
			print("Liste d evenements : ") 
			print(self.eventList)
			print("Coeffs de MAJ // CoeffREV = " + str(IdxRev) + " // CoeffRPK = " + str(IdxRPK))
		
		else:
			
			#absolute modification
			e = event.EventAddAbsoluteData(valRev, valRPK, self.index.column()+1, yld, self.parentTable.flow, self.debug)
			self.eventList[self.index.column()] = e
			print("Liste d evenements : ") 
			print(self.eventList)
			print("Nouvelles absolute values de MAJ // Rev = " + str(valRev) + " // RPK = " + str(valRPK))	
			
		# if self.debug == True:
				# print("Value sent to the action handler is : " + str(self.cy))
		
		self.modifFlag = False
		print("fin de creation d evenement et indicateur self.modifFlag = " + str(self.modifFlag))	

			
	
	def callbackModifCY(self):
		print("entre dans fonction callbackModifCY")
		""" callback function launched once self.cy_LE has been modified """
		
		# for debugging purpose
		# if self.debug == True:
			# print("Callback on cy modification")
		
		# update data model in the system
		tmp = self.cy_LE.text().toFloat()
		# print("Callback on cy modification : self.cy = " + str(self.convertFloatToString(tmp[0] * 1000)))
		if (tmp[1] == True) and (tmp[0]>=0):
			if self.header[:5] == "Yield":
				self.cy =  tmp[0] / 100
			else:
				self.cy = tmp[0] * 1000
		else:
			self.cy_LE.setText(self.convertFloatToString(self.cy))
		
		print("Callback on cy modification : self.cy = " + str(self.cy))
		
		
		# tell the class something has been modified
		self.modifFlag = True
		print("ModifFlag mis a True dans callbackmodify")
		
		# update the YoY
		self.yoy_LE.setValue(self.calcyoY(self.cy, self.ref))
		
	
		
		
	def validate(self):
		# print("entre dans validate")
		# send all events to the list of actions pending
		for e in self.eventList:
			if e != []:
				self.sidePanel.user_interaction.addPendingActions(e)
				self.actionSent = 1
		
	def validateAndClose(self):
		# update the gui
		self.update_gui()
		
		# add event if not null
		self.validate()
		
		#close the window
		self.done(0)
		
	def changePosition(self, left_or_right):
		# print("entre dans fonction changePosition")
		""" Validate - function used when button to the right or the left are being pressed / True means to the right , False to the left"""
		# update gui before moving to next month
		self.update_gui()
		
		# initialization of flag
		self.modifFlag = False
		# print("self.modifFlag = False dans ChangePosition")
		
		# if (self.debug):
			# print("Moving to " + str(left_or_right))
			
		# find next index.
		col = self.index.column()
		if (left_or_right) and (col < 11):
			col += 1
		elif not (left_or_right):
			col -= 1
		
		# do nothing if col < 0
		if col >= 0:
			new_index = self.index.sibling(self.index.row(), col)
			
			# fetch new data
			self.initData(new_index)
			if (self.debug):
				print("Updating data for month :" + str(col+1))
			
			# update display
			self.updateDisplay()
					
	def moveToRight(self):
		self.changePosition(True)
		
	def moveToLeft(self):
		self.changePosition(False)
		
		
	def keyPressEvent(self, e):
		"""handling key strokes """
		# closing window on escape
		if e.key() == Qt.Key_Escape:
			self.validateAndClose()
		
		# validate result on enter	
		if e.key() == Qt.Key_Enter:
			print("key enter pressed")
			#update the gui
			self.update_gui()
		
		# moving to next data
		elif e.key() == Qt.Key_Right:
			print("right botton pressed")
			self.moveToRight()
		
		#moving to previous data
		elif e.key() == Qt.Key_Left:
			print("left botton pressed")
			self.moveToLeft()