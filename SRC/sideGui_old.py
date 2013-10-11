import sys

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
	def __init__(self, fm, core, parent, status, debug=True):
		QWidget.__init__(self)

		#status bar
		self.status = status
		self.parent = parent
		self.layout = QHBoxLayout()

		# user interaction
		self.user_interaction = UserInteraction(core, self.status, self, debug)
		self.layout.addWidget(self.user_interaction)
		# reference
		self.layout.addWidget(ReferenceWidget(core, self, debug))
		# route perimeter
		self.layout.addWidget(PerimeterSelection(core, fm, self))

		self.setLayout(self.layout)
		self.sizeHint()
		self.setMinimumSize(100,10)



class UserInteraction(QWidget):
#class UserInteraction(QGroupBox):
		""" a class for the user to interact with the database / core engine
			this class allow to apply all pending actions to the database behind all calculations
		"""
		def __init__(self, core, status, parent, debug=True, *args):
#			QGroupBox.__init__(self, *args)
			QWidget.__init__(self, *args)			

			self.debug = debug
			self.parent = parent
			
			# core engine to process all requests
			self.core = core
			self.nbrPending = 0

			
			#status bar
			self.status = status

#			self.setTitle(QString("User actions"))
			self.layout = QVBoxLayout()
			#set title
			self.layout.addWidget(QLabel("<b>User actions</b>"))

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
			validate = QMessageBox.warning(self, "Validation required", "Are you sure to proceed ?", QMessageBox.Cancel | QMessageBox.Ok)
			if validate == QMessageBox.Ok:
				# enable validation
				validation = True
			else:
				validation = False
			if (self.nbrPending > 0) and (validation):
				res = self.core.process_events()
				if res == 0:
					self.status.showMessage("Actions saved")
					#zero the display
					self.zeroPending()
					if (self.debug):
						print("Actions saved")
				else:
					self.status.showMessage("Error processing data")
					print("Error processing data")
		
		
		def saveActionsNoValidation(self):
			self.status.showMessage("Processing actions")
			
			if self.nbrPending > 0 :
				res = self.core.process_events()
				if res == 0:
					self.status.showMessage("Actions saved")
					#zero the display
					self.zeroPending()
					if (self.debug):
						print("Actions saved")
				else:
					self.status.showMessage("Error processing data")
					print("Error processing data")
		
		
		def discardActions(self):
			if self.nbrPending > 0:
				#clear core engine
				self.core.clear_events()
				#zero the display
				self.zeroPending()
				self.status.showMessage("Actions discarded")
				#re get all data from db
				self.core.get_data_CY()
				# update the display
				self.parent.parent.tabsWidget.updateData()
				self.parent.parent.tabsWidget.updateTabs()
				
				if (self.debug):
					print("Actions discarded")



#class ReferenceWidget(QGroupBox):
class ReferenceWidget(QWidget):
	""" allow selection of the type of ref for calculation and setting parameters for the ref"""
	def __init__(self, core, parent, debug=True):
#		QGroupBox.__init__(self, parent)
		QWidget.__init__(self,parent)

		self.core = core
		self.parent = parent
		self.debug = debug

#		self.setTitle(QString("Reference"))

		self.layout = QGridLayout()

		#add a title
		self.layout.addWidget(QLabel("<b>Reference</b>"),0,0)

		#selecting if reference is retreated or not
		self.layout.addWidget(QLabel(QString("Choose type of reference"), self),1,0)
		self.trButton = QRadioButton("Retreated", self)
		self.ntrButton = QRadioButton("Non retreated", self)
		self.layout.addWidget(self.trButton,2,0)
		self.layout.addWidget(self.ntrButton,3,0)

		#set treatment according to core engine parameter
		self.changeTreatment(self.core.treatment)

		#which reference to choose
		self.layout.addWidget(QLabel("Choose reference data", self),0,1)
		self.listRef = QListWidget(self)
		# add the reference table in the widget
		self.addReference(core)
		self.layout.addWidget(self.listRef,1,1,-1,1)

		#select first element in the list by default
		self.listRef.setCurrentItem(self.listRef.item(0))
		
		
		#connect slot and signal
		#reference treatment
		self.connect(self.trButton, SIGNAL("toggled(bool)"), self.changeTreatmentEventTr)
		self.connect(self.ntrButton, SIGNAL("toggled(bool)"), self.changeTreatmentEventNTr)
		# reference data
		self.connect(self.listRef, SIGNAL("currentItemChanged(QListWidgetItem *,QListWidgetItem *)"), self.changeReference)


		self.setLayout(self.layout)

	def addReference(self, core):
		""" add the reference table to be used """
		# retrieve the list of reference form the core engine

		lst = core.referenceDict
		for nick_name, table in lst.items():
				if table != "DATA_RAW":
					self.listRef.addItem(QListWidgetItem(nick_name, self.listRef))

	def changeReference(self, itemOri, itemFin):
		""" change reference in the data sent to the GUI """
		

		#new reference
		ref = str(itemOri.text().toUtf8())
		if self.debug == True:
			print("reference changed to  " + ref)

		#change ref in the core and get  data to the core
		self.core.setRef(ref)

		#update layout - sending data to the gui
		if self.debug == True:
			print("Sending update to display")
		self.parent.status.showMessage("reference changed")
		self.parent.parent.tabsWidget.changeRef()
		

	def changeTreatment(self, treatment):
		if treatment == STATIC.NON_RETREATMENT:
			self.ntrButton.setChecked(True)
		else:
			self.trButton.setChecked(True)

	
	def _changeTreatmentEvent(self, bool):
		""" modify treatment in the core """
		if bool == True:
			self.core.set_treatment(STATIC.RETREATMENT)
		else :
			self.core.set_treatment(STATIC.NON_RETREATMENT)
		
		# update the tabs
		self.parent.parent.tabsWidget.changeRef()
		self.parent.status.showMessage("reference treatment changed")
	
	def changeTreatmentEventTr(self, bool):
		if bool == True:
			self._changeTreatmentEvent(True)

	def changeTreatmentEventNTr(self, bool):
		if bool == True:
			self._changeTreatmentEvent(False)		
	
#class PerimeterSelection(QGroupBox):
class PerimeterSelection(QWidget):
	""" allow to select the route perimeter """
	def __init__(self, core, fm, parent, debug = True):
#		QGroupBox.__init__(self, parent)
		QWidget.__init__(self, parent)
		self.parent = parent
		self.debug = debug
		self.fm = fm
		self.core = core
		self.validation = True
		self.mechanicalMove = False

#		self.setTitle(QString("Route perimeter"))
		self.layout = QGridLayout()

		#title
		self.layout.addWidget(QLabel("<b>Route perimeter</b>"),0,0)

		# add the found hierarchy in the list
		self.listPerimeter = QListWidget(self)
		
		self.listPerimeter.setSelectionMode(QAbstractItemView.SingleSelection)
		# self.listPerimeter.setSelectionMode(QAbstractItemView.NoSelection)
		
		self.defineList(fm)

		
		
		self.layout.addWidget(self.listPerimeter,1,0,1,-1)

		self.reload = QPushButton("Reload list")
		self.reload.sizeHint()
		self.layout.addWidget(self.reload,0,1)
		
		self.setLayout(self.layout)

		#set the first item by default
		self.listPerimeter.setCurrentItem(self.listPerimeter.item(0))

		# signal & slots
		self.connect(self.listPerimeter, SIGNAL("currentItemChanged(QListWidgetItem *,QListWidgetItem *)"), self.changePerimeter)
		# self.connect(self.listPerimeter, SIGNAL("currentItemChanged(QListWidgetItem *,QListWidgetItem *)"), self.currentItemChanged)
		self.connect(self.reload, SIGNAL("clicked()"), self.actionReload)

		
	def defineList(self, fm):
		""" get the lists of files within the directory specified """
		# remove all if necessary
		self.listPerimeter.clear()
		# add the list
		for i in fm.getHierarchies():
			self.listPerimeter.addItem(QListWidgetItem(i, self.listPerimeter))

	def changePerimeter(self, item, itemInit):
	# def currentItemChanged(self, item, itemInit):
		""" change perimeter in the data sent to the GUI / clear all pending actions as well"""

		if self.mechanicalMove == False:
			# pending actions still not processed
			if len(self.core.events_list) > 0:
				#ask for validation
				
				validate = QMessageBox.warning(self, "Validation required", "Pending actions have been processed\nApply or Discard actions before changing perimeter :", QMessageBox.Cancel | QMessageBox.Ok)
				# validate = QMessageBox(QMessageBox.Warning, "Validation required", "Pending actions have been processed\nApply or Discard actions before changing perimeter :", QMessageBox.Yes | QMessageBox.No)
				# validate.setButtonText(QMessageBox.Yes, str("Apply"))
				# validate.setButtonText(QMessageBox.No, str("Discard")
				# validate.setDefaultButton(QMessageBox.No)
				
				if validate == QMessageBox.No:
					# enable validation
					self.validation = True
					# clear actions list
					self.parent.user_interaction.discardActions()
				elif validate == QMessageBox.Yes:
					# enable validation
					self.validation = True
					# save actions list in db
					self.parent.user_interaction.saveActionsNoValidation()
				
				else:
					self.validation = False


			if self.validation == True:

				if self.debug == True:
					print("Perimeter changed")

				#clear rfs list in the db
				self.core.clear_rfs_used()

				file2read = str(item.text().toUtf8())

				# add lines to the db
				lstLines = self.fm.getSublines(file2read)
				for line in lstLines:
					self.core.set_rfs_used(line)

				# update the number of routes in the core
				self.core.countNumberOfRoutes()

				# retrieve new data
				self.core.get_data_CY()
				self.core.get_data_ref()

				self.parent.parent.tabsWidget.updateData()


				# send message to GUI status bar
				self.parent.status.showMessage("Perimeter changed")

				self.validation = True

			else:
				# reselect previous item
				self.validation = True
				self.mechanicalMove = True
				if self.debug == True:
					print("Switching back to : " + itemInit.text())
				# self.listPerimeter.blockSignals(True)
				# self.listPerimeter.clearSelection()
				# itemInit.setSelected(True)
				# self.listPerimeter.setCurrentItem(itemInit)
				self.listPerimeter.setItemSelected(itemInit, True)
				# self.listPerimeter.setCurrentRow(self.listPerimeter.row(itemInit))
				# self.listPerimeter.selectionModel().select(self.listPerimeter.currentIndex(), QItemSelectionModel.Select);
				self.listPerimeter.update()
				#self.listPerimeter.setItemSelected(itemInit, True)
				
				# self.listPerimeter.blockSignals(False)
				print(self.listPerimeter.currentItem().text() +  " "  + str(self.listPerimeter.currentIndex().row()))

		else:
			self.mechanicalMove = False
			if self.debug == True:
				print("Set mechanical move to False")
	
	def actionReload(self):
		""" function loaded when the user want to reload the list of routes available """
		self.mechanicalMove = True
		# reload hierarchies
		self.fm.loadHierarchies()
		# get the new one and put it on the widget
		self.defineList(self.fm)
		self.mechanicalMove = False
