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
		# 2 lines representing forecast and ref
		#	Type of data *
		#		Flow * 5
		#			yield * 3
		#				month * 13
		self.tableData = []

		# define the header to be display verticaly
		self.vHeader = self.setVHeader()

		#get the data right (ie define tableData )
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

		# data scheme of the array
		#	0  ASK HY Data
		#	1		  Ref
		#	2		  YoY
		#	3  ASK LY Data
		#	4		  Ref
		#	5		  YoY
		#	6  ASK AY Data
		#	7		  Ref
		#	8		  YoY
		#	9  ASK HY Data
		#	10		  Ref
		#	11		  YoY
		#	12  ASK LY Data
		#	13		  Ref
		#	14		  YoY
		# 	15 ASK AY Data
		#	16		  Ref
		#	17		  YoY







		for data in ["ASK", "RPK", "LF", "yield", "Rev"]:
			for yld in equivYield:
				# for forecast
				self.tableData.append(self.core.DATA_FCST[equivData[data]][equivFlow[flow]][equivYield[yld]][1:17])
				# for ref
				self.tableData.append(self.core.DATA_REF[equivData[data]][equivFlow[flow]][equivYield[yld]][1:17])
				# for yoy
				self.tableData.append([None]*17)

		# insert RASK data
		for yld in equivYield:
			# for forecast
			self.tableData.append([None]*17)
			# for ref
			self.tableData.append([None]*17)
			# for yoy
			self.tableData.append([None]*17)


	def setVHeader(self):
		"""set the vHeader right - development only """
		vHeader = []
		for data in VERTICAL_HEADER:
					vHeader.append(data)
		return vHeader

class TableData(QAbstractTableModel):
	""" table displaying all the data """
	""" this table requires a big array containing all required data """

	def __init__(self, datain, vheader, hheader, parent=None, *args):
		""" define array containing all the data and all the headers"""
		QAbstractTableModel.__init__(self, parent, *args)
		self.arraydata = datain
		self.vheader = vheader
		self.hheader = hheader

	def rowCount(self, parent):
		#return 27
		return len(self.arraydata)

	def columnCount(self, parent):
		return len(self.arraydata[0])

	def data(self, index, role):
		""" retrieve data within the data container """
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


	def setDataConsistency(self):
		""" allow to calculate links within the array representing the table"""


		# RPK consistency (9 first lines)
		# -------------------------------
		#for m in equivMonth:
		#	self.arraydata[



