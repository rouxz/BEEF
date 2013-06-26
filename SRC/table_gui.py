import sys

from static import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from mainGui import *
from file_manager import *

# data to display
my_array = [['00','01','02'],
			['10','11','12'],
			['20','21','22']]

# ###################################
#
#    DATA HANDLING WITHIN THE GUI   #
#
# ###################################


class Tabs(QTabWidget):
	""" class for defining the tabs including all the tables """

	def __init__(self, core, parent):
		QTabWidget.__init__(self, parent)

		self.setMinimumSize(300,300)
		for flow in equivFlow:
			self.addTab(TableWidget(core, flow, parent), flow)
		#self.minimumSizeHint()





class TableWidget(QWidget):
	""" class describing the table of data used in the several tabs """
	
	
	def __init__(self, core, flow, parent):
		QWidget.__init__(self, parent)
		# set the core engine
		self.core = core

		# internal table detaining all necessary information
		self.tableData = []

		# define the header to be display verticaly
		self.vHeader = self.setVHeader()

		#get the data right
		self.getAllData(flow)

		#initiate the all widget
		self.initUI(flow)

	def initUI(self,flow):

		# define the table displayed
		self.table = QTableView()
		# define the table to be used
		
		self.tableModel = TableData(self.tableData, self.vHeader, TABLE_TITLE, self)
		
		#define the model to be used by the table
		self.table.setModel(self.tableModel)

		 # set the minimum size
		self.table.setMinimumSize(800, 300)

		# set the font
		self.table.setFont(QFont("Courier New", 8))

		

		# set horizontal header properties
		#self.table.horizontalHeader().setStretchLastSection(True)

		# set column width to fit contents
		#self.table.resizeColumnsToContents()

		# set row height
		nrows = len(my_array)
		for row in xrange(nrows):
			self.table.setRowHeight(row, 18)

		#add the table within a layout
		self.layout = QVBoxLayout(self)
		self.layout.addWidget(self.table)
		self.setLayout(self.layout)

		#self.center()
		#self.show()

	def center(self):

		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def getAllData(self, flow):
		"""retrieve all necessary data from core engine and put them into internal table """

		# take all the data
		# ----------------

		for data in ["ASK","RPK","Rev"]:
			for yld in equivYield:
				# for forecast
				self.tableData.append(self.core.DATA_FCST[equivData[data]][equivFlow[flow]][equivYield[yld]][1:13])
				# for ref
				self.tableData.append(self.core.DATA_REF[equivData[data]][equivFlow[flow]][equivYield[yld]][1:13])

	def setVHeader(self):
		"""set the vHeader right - development only """
		vHeader = []
		for data in ["ASK","RPK","Rev"]:
			for yld in equivYield:
				for nick_name in ["Data", "Ref", "YoY"]:
					vHeader.append(data + " - " + yld + " " + nick_name)
		return vHeader

class TableData(QAbstractTableModel):
	""" table for including all data within a table """

	def __init__(self, datain, vheader, hheader, parent=None, *args):
		QAbstractTableModel.__init__(self, parent, *args)
		self.arraydata = datain
		self.vheader = vheader
		self.hheader = hheader
		
	def rowCount(self, parent):
		return len(self.arraydata)

	def columnCount(self, parent):
		return len(self.arraydata[0])

	def data(self, index, role):
		if not index.isValid():
			return QVariant()
		elif role != Qt.DisplayRole:
			return QVariant()
		return QVariant(self.arraydata[index.row()][index.column()])

	def headerData(self, section, orientation, role):
		if role != Qt.DisplayRole:
			return QVariant()
		if orientation == Qt.Vertical:
			return QVariant(self.vheader[section])
		if orientation == Qt.Horizontal:
			return QVariant(self.hheader[section])

