﻿import sys

import static as STATIC
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from mainGui import *
from file_manager import *

# ###########################################
#
#	INTERFACE ELEMENTS (BUTTONS...)
#
# ############################################


class SidePanel(QWidget):
	""" a class for including a side panel allowing to select several options in the gui """
	def __init__(self, fm, core, parent, status):
		QWidget.__init__(self)
		
		#status bar
		self.status = status
		
		self.layout = QVBoxLayout()
		
		# user interaction
		self.user_interaction = UserInteraction(core, self.status, self)
		self.layout.addWidget(self.user_interaction)
		# reference
		self.layout.addWidget(ReferenceWidget(core, self))
		# route perimeter
		self.layout.addWidget(PerimeterSelection(fm, self))

		self.setLayout(self.layout)
		self.sizeHint()
		self.setMinimumSize(100,10)
		


class UserInteraction(QGroupBox):
		""" a class for the user to interact with the database / core engine 
			this class allow to apply all pending actions to the database behind all calculations
		"""
		def __init__(self, core, status, *args):
			QGroupBox.__init__(self, *args)
			
			# core engine to process all requests
			self.core = core
			self.nbrPending = 0
			
			#status bar
			self.status = status
			
			self.setTitle(QString("User actions"))
			self.layout = QVBoxLayout()

			#show number of pending actions
			self.labelNbrPending = QLabel(QString("Pending actions : 0"), self)
			self.layout.addWidget(self.labelNbrPending)

			#save button
			self.save = QPushButton("Apply", self)
			self.layout.addWidget(self.save)
			#discard button
			self.discard = QPushButton("Discard", self)
			self.layout.addWidget(self.discard)

			#connect slots and signals
			self.save.connect(self.save, SIGNAL("clicked()"), self.saveActions)
			self.discard.connect(self.discard, SIGNAL("clicked()"), self.discardActions)
			
			self.setLayout(self.layout)

		def setNumberPending(self, num):
			""" update the display of the number of pending actions with the required number"""
			self.nbrPending = num
			self.labelNbrPending.setText(STATIC.PENDING_LABEL + str(num))
		
		def incrementPending(self):
			self.setNumberPending(self.nbrPending + 1)
		
		def zeroPending(self):
			self.setNumberPending(0)
		
		def addPendingActions(self, action):
			""" add an action to the core list """
			self.incrementPending()
			self.status.showMessage("Action added")
			self.core.add_event(action)

			
		def saveActions(self):
			self.status.showMessage("Processing actions")
			#print("Processing actions")
			res = self.core.process_events()
			if res == 0:
				self.status.showMessage("Actions saved")
				#zero the display
				self.zeroPending()
				print("Actions saved")
			else:
				self.status.showMessage("Error processing data")
				print("Error processing data")
		
		def discardActions(self):
			#clear core engine
			self.core.clear_events()
			#zero the display
			self.zeroPending()
			self.status.showMessage("Actions discarded")
			#re get all data from db
			self.core.get_data_CY()
			print("Actions discarded")

		

class ReferenceWidget(QGroupBox):
	""" allow selection of the type of ref for calculation and setting parameters for the ref"""
	def __init__(self, core, parent):
		QGroupBox.__init__(self, parent)
		
		self.core = core
		self.parent = parent
		
		self.setTitle(QString("Reference"))

		self.layout = QVBoxLayout()

		#selecting if reference is retreated or not
		self.layout.addWidget(QLabel(QString("Choose type of reference"), self))
		self.trButton = QRadioButton("Retreated", self)
		self.ntrButton = QRadioButton("Non retreated", self)
		self.layout.addWidget(self.trButton)
		self.layout.addWidget(self.ntrButton)
		
		#set treatment according to core engine parameter
		self.changeTreatment(self.core.treatment)
		
		#which reference to choose
		self.layout.addWidget(QLabel("Choose reference data", self))
		self.listRef = QListWidget(self)
		# add the reference table in the widget
		self.addReference(core)
		self.layout.addWidget(self.listRef)

		#connect slot and signal
		self.connect(self.listRef, SIGNAL("currentItemChanged(QListWidgetItem *,QListWidgetItem *)"), self.changeReference)
		
		
		self.setLayout(self.layout)

	def addReference(self, core):
		""" add the reference table to be used """
		# retrieve the list of reference form the core engine

		lst = core.referenceList
		for table in lst:
				if table[0] != "DATA_RAW":
					self.listRef.addItem(QListWidgetItem(table[1], self.listRef))
					
	def changeReference(self):
		""" change reference in the data sent to the GUI """
		print("reference changed")
		self.parent.status.showMessage("reference changed")
		
	def changeTreatment(self, treatment):
		if treatment == STATIC.NON_RETREATMENT:
			self.ntrButton.setChecked(True)
		else:
			self.trButton.setChecked(True)
			
			
class PerimeterSelection(QGroupBox):
	""" allow to select the route perimeter """
	def __init__(self, fm, parent):
		QGroupBox.__init__(self, parent)
		
		self.parent = parent
		
		self.setTitle(QString("Route perimeter"))
		self.layout = QVBoxLayout()
		
		# add the found hierarchy in the list
		self.listPerimeter = QListWidget(self)
		self.defineList(fm)
		
		self.layout.addWidget(self.listPerimeter)
		

		self.setLayout(self.layout)

		# signal & slots
		self.connect(self.listPerimeter, SIGNAL("currentItemChanged(QListWidgetItem *,QListWidgetItem *)"), self.changePerimeter)
		
		
	def defineList(self, fm):
		""" get the lists of files within the directory specified """
		for i in fm.getHierarchies():
			self.listPerimeter.addItem(QListWidgetItem(i, self.listPerimeter))
			
	def changePerimeter(self):
		""" change perimeter in the data sent to the GUI / clear all pending actions as well"""
		print("Perimeter changed")
		self.parent.status.showMessage("Perimeter changed")
