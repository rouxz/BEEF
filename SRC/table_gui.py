﻿import sys

from static import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from mainGui import *
from file_manager import *
import re

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
		self.vHeader = VERTICAL_HEADER

		#get the data right (ie define tableData )
		self.retrieveData(flow)

		# set consistency for all data
		self.setDataConsistency()

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

	def retrieveData(self, flow):
		"""retrieve all necessary data from core engine and put them into internal array """

		# take all the data
		# ----------------

		#populate ASK and RPK
		for data in ["ASK", "RPK"]:
			for yld in ARRAY_YIELD:
				# for forecast
				self.tableData.append(self.core.DATA_FCST[ARRAY_DATA.index(data)][equivFlow[flow]][ARRAY_YIELD.index(yld)][1:18])
				# for ref
				self.tableData.append(self.core.DATA_REF[ARRAY_DATA.index(data)][equivFlow[flow]][ARRAY_YIELD.index(yld)][1:18])
				# for yoy
				self.tableData.append([0]*17)



		# populate LF data with blank line
		for yld in ARRAY_YIELD:
			# for forecast
			self.tableData.append([0]*17)
			# for ref
			self.tableData.append([0]*17)
			# for yoy
			self.tableData.append([0]*17)

		# populate yield data with blank line
		for yld in ARRAY_YIELD:
			# for forecast
			self.tableData.append([0]*17)
			# for ref
			self.tableData.append([0]*17)
			# for yoy
			self.tableData.append([0]*17)

		# populate rev data
		for yld in ARRAY_YIELD:
			# for forecast
			self.tableData.append(self.core.DATA_FCST[ARRAY_DATA.index("Rev")][equivFlow[flow]][ARRAY_YIELD.index(yld)][1:18])
			# for ref
			self.tableData.append(self.core.DATA_REF[ARRAY_DATA.index("Rev")][equivFlow[flow]][ARRAY_YIELD.index(yld)][1:18])
			# for yoy
			self.tableData.append([0]*17)

		# populate RASK data with blank line
		for yld in ARRAY_YIELD:
			# for forecast
			self.tableData.append([0]*17)
			# for ref
			self.tableData.append([0]*17)
			# for yoy
			self.tableData.append([0]*17)

		#check array consistency
		#for r in VERTICAL_HEADER:
		#	print(r + " len " + str(len(self.tableData[VERTICAL_HEADER.index(r)])))

	def setDataConsistency(self):
		""" allow to calculate links within the array representing the table"""

		regexp1 = re.compile("(Rev|RPK).(HY|LY).(?!YoY).*")

		# calculation on total per line for relevant lines (RPK, REV) for HY and LY
		# 1- annual
		# 2- quarters
		for r in VERTICAL_HEADER:
			if regexp1.match(r) != None:
				# annual sum
				sum = 0
				for i in range(0,12):
					sum += self.tableData[VERTICAL_HEADER.index(r)][i]
				self.tableData[VERTICAL_HEADER.index(r)][12] = sum
				# quarterly sum
				for q in ARRAY_QUARTERS:
					sum = 0
					for m in q:
						sum += self.tableData[VERTICAL_HEADER.index(r)][m-1]
					self.tableData[VERTICAL_HEADER.index(r)][13 + ARRAY_QUARTERS.index(q)] = sum
					
		# 3 - calculate data for AY RPK and REV
		regexp2 = re.compile("(Rev|RPK).AY.(?!YoY).*")
		#for r in VERTICAL_HEADER:
		#	#looking for AY info 
		#	if regexp2.match != None:
		#		#summing LY and HY
		#		for i in range(0,18):
		#			if r[:3] = "Rev":
		#				self.tableData[VERTICAL_HEADER.index(r)][i]  =  self.tableData[VERTICAL_HEADER.index(r)] 
		
		
		# 3 - populate yield, lF and RASK

		# 4 - calculate YoY Y-Y

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








