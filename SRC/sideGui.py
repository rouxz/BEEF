import sys

from static import *
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
	def __init__(self, fm, core, parent):
		QWidget.__init__(self)
		self.layout = QVBoxLayout()
		# user interaction
		self.layout.addWidget(UserInteraction(self))
		# reference
		self.layout.addWidget(ReferenceWidget(core, self))
		# route perimeter
		self.layout.addWidget(PerimeterSelection(fm, self))

		self.setLayout(self.layout)
		self.sizeHint()
		self.setMinimumSize(50,10)
		


class UserInteraction(QGroupBox):
		""" a class for the user to interact with the database / core engine """
		def __init__(self, *args):
			QGroupBox.__init__(self, *args)
			self.setTitle(QString("User actions"))
			self.layout = QVBoxLayout()

			#show number of pending actions
			self.layout.addWidget(QLabel(QString("Pending actions : 0"), self))

			#save button
			self.layout.addWidget(QPushButton("Save", self))
			#discard button
			self.layout.addWidget(QPushButton("Discard", self))


			self.setLayout(self.layout)



class ReferenceWidget(QGroupBox):
	""" allow selection of the type of ref for calculation and setting parameters for the ref"""
	def __init__(self, core, parent):
		QGroupBox.__init__(self, parent)
		self.setTitle(QString("Reference"))

		self.layout = QVBoxLayout()

		#selecting if reference is retreated or not
		self.layout.addWidget(QLabel(QString("Choose type of reference"), self))
		self.trButton = QRadioButton("Retreated", self)
		self.ntrButton = QRadioButton("Non retreated", self)
		self.layout.addWidget(self.trButton)
		self.layout.addWidget(self.ntrButton)
		
		#which reference to choose
		self.layout.addWidget(QLabel("Choose reference data", self))
		self.listRef = QListWidget(self)
		# add the reference table in the widtet
		self.addReference(core)
		self.layout.addWidget(self.listRef)

		
		
		self.setLayout(self.layout)

	def addReference(self, core):
		""" add the reference table to be used """
		# retrieve the list of reference form the core engine
		lst = core.referenceList
		
		for i in lst:
			if i.TABLE != "DATA_RAW":
				self.listRef.addItem(QListWidgetItem(i.NICK_NAME, self.listRef))
		
class PerimeterSelection(QGroupBox):
	""" allow to select the route perimeter """
	def __init__(self, fm, parent):
		QGroupBox.__init__(self, parent)
		self.setTitle(QString("Route perimeter"))
		self.layout = QVBoxLayout()
		
		# add the found hierarchy in the list
		self.listPerimeter = QListWidget(self)
		self.defineList(fm)
		
		self.layout.addWidget(self.listPerimeter)
		

		self.setLayout(self.layout)

	def defineList(self, fm):
		""" get the lists of files within the directory specified """
		for i in fm.getHierarchies():
			self.listPerimeter.addItem(QListWidgetItem(i, self.listPerimeter))
