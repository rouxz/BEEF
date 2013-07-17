import sys

from static import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from mainGui import *
from file_manager import *
from window_modif import *
import re


# regexp
# ------
DATA_FROM_DB = re.compile("(Rev|RPK|ASK).(HY|LY).(?!YoY).*")

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



	def __init__(self, core, sidePanel, parent):
		QTabWidget.__init__(self, parent)

		self.parentWidget = parent

		#for user interactions
		self.sidePanel = sidePanel

		#list of all the displayed tabs
		self.tabs = []

		i = 0

		# add new tabs
		for flow in equivFlow:
			self.tabs.append(MyTableView(core, flow, self.sidePanel, parent))
			self.addTab(self.tabs[i], flow)
			i = i +1

		self.setUI()

	def setUI(self):
		self.setMinimumSize(300,300)


	def updateTabs(self):
		""" update the data displayed in all the present tabs"""
		for tab in self.tabs:
			tab.updateDisplay()


class TableData(QAbstractTableModel):
	""" all the data bying displayed in the tabs """
	""" this table requires a big array containing all required data """

	def __init__(self, datain, vheader, hheader, parent=None, *args):
		""" define array containing all the data and all the headers"""
		QAbstractTableModel.__init__(self, parent, *args)
		self.arraydata = datain
		self.vheader = vheader
		self.hheader = hheader

	def rowCount(self, parent):
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

	def getData(self, r, c):
		""" retrieve data within the data container simple way as a string"""
		return self.qstr2str(self.data(self.index(r, c), Qt.DisplayRole))

	def getDataFloat(self, r, c):
		""" retrieve data within the data container simple way as a string"""
		return float(self.qstr2str(self.data(self.index(r, c), Qt.DisplayRole)))

	def headerData(self, section, orientation, role):
		if role != Qt.DisplayRole:
			return QVariant()
		if orientation == Qt.Vertical:
			return QVariant(self.vheader[section])
		if orientation == Qt.Horizontal:
			return QVariant(self.hheader[section])

	def setData(self, index, value):
		""" change data in the array containing all the required information """
		if index.isValid():
			self.arraydata[index.row()][index.column()] = value
			#show to the world the update
			self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)


	def setDataNoDisplayUpdate(self, row, col, value):
		"""change data in the data model without updating the gui """
		self.arraydata[row][col] = value

	def updateDisplay(self):
		self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), self.index(0,0), self.index(len(VERTICAL_HEADER),len(TABLE_TITLE)))

	def setData2(self, row, col, value):
		""" test only """
		self.setData(self.index(row, col), value)


	def index(self, row, col, parent = QModelIndex()):
		""" redefinition of the index function """
		return self.createIndex(row, col)

	#converting Qstring to float
	def qstr2str(self, qstr):
		return str(qstr.toString()).strip()

	# def flags(self, index):
		# if index.isValid() and index.row < self.rowCount(None) and index.col < self.columCount(None):
			# return Qt.ItemFlags(Qt.ItemIsEditable | Qt.ItemIsSelectable |Qt.ItemIsEnabled)
		# else:
			# return Qt.ItemFlags(Qt.ItemIsSelectable |Qt.ItemIsEnabled)

class MyTableView(QTableView):
	""" table specialisation of QTableView displaying all the data and calculated KPI fetched from db"""

	def __init__(self, core, flow, sidePanel, parent, debug = True):

		QTableView.__init__(self)

		#core engine
		self.core = core

		#sidePanel
		self.sidePanel = sidePanel

		#debug parameter
		self.debug = debug

		#flow represented in this table
		self.flow =  flow


		# define the data to be used
		# self.tableData = [[0] * len(TABLE_TITLE)]*len(VERTICAL_HEADER)
		self.tableData = []
		for r in range(len(VERTICAL_HEADER)):
			self.tableData.append([])
			for c in range(len(TABLE_TITLE)):
				self.tableData[r].append(0)
		# self.retrieveData_()

		# set consistency for all data
		# self.setDataConsistency()

		#define dataModel for MVC
		self.tableModel = TableData(self.tableData, VERTICAL_HEADER, TABLE_TITLE, parent)

		#define the model to be used by the table
		self.setModel(self.tableModel)

		# set the font
		self.setFont(QFont("Courier New", 8))

		# get data from coreengine
		self.retrieveData()

		 # set the minimum size
		# self.setMinimumSize(1000, 300)



		# set row height
		# nrows = len(my_array)
		# for row in xrange(nrows):
			# self.table.setRowHeight(row, 18)

		#connecting events
		#-----------------

		#new way
		self.connect(self, SIGNAL("doubleClicked(QModelIndex)"), self.cell_clicked_event)
		#self.connect(self, SIGNAL("doubleclicked(QModelIndex)"), self.affiche_coordo)

	def retrieveData(self):
		""" get all data from core engine """

		flw = ARRAY_FLOW.index(self.flow)

		for r in VERTICAL_HEADER:
			row = VERTICAL_HEADER.index(r)

			for c in range(len(TABLE_TITLE)):
				# print(str(r) + "-" + str(c) + " " )
				if DATA_FROM_DB.match(r):
					end = r[-3:].strip()
					yld = ARRAY_YIELD.index(r[4:6].strip())
					type = ARRAY_DATA.index(r[:3].strip())
					if c < 12: #data is a month
						# data is either Rev or RPK for CY or ref
						if end == "CY":
							#print(self.flow + " r : " + r + " - m:" + str(c+1) + " v: "+   str(self.core.DATA_FCST[type][flw][yld][c + 1]))
							self.tableModel.setDataNoDisplayUpdate(row, c, self.core.DATA_FCST[type][flw][yld][c + 1] )
							# self.tableModel.setData(self.tableModel.index(row,c), self.core.DATA_FCST[type][flw][yld][c + 1])
							# print(str(self.tableModel.index(row,c).data().toString()))
						elif end == "Ref":
							self.tableModel.setDataNoDisplayUpdate(row, c, self.core.DATA_REF[type][flw][yld][c + 1] )
							# self.tableModel.setData(self.tableModel.index(row,c), self.core.DATA_REF[type][flw][yld][c + 1])
					else:
						self.tableModel.setDataNoDisplayUpdate(row, c, 0)
						# self.tableModel.setData(self.tableModel.index(row,c),0)
				else:
						self.tableModel.setDataNoDisplayUpdate(row, c, 0)
						# self.tableModel.setData(self.tableModel.index(row,c),0)

		# calcultate all totals
		self.setDataConsistency()


		#update display
		self.tableModel.updateDisplay()



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
					sum += float(self.tableModel.getData(VERTICAL_HEADER.index(r),i))
				self.tableModel.setDataNoDisplayUpdate(VERTICAL_HEADER.index(r), 12, sum)
				# quarterly sum
				for q in ARRAY_QUARTERS:
					sum = 0
					for m in q:
						sum += float(self.tableModel.getData(VERTICAL_HEADER.index(r), m - 1))
					self.tableModel.setDataNoDisplayUpdate(VERTICAL_HEADER.index(r), 13 + ARRAY_QUARTERS.index(q), sum)

		# 3 - calculate data for AY RPK and REV
		regexp2 = re.compile("(Rev|RPK).AY.(?!YoY).*")
		for r in VERTICAL_HEADER:
			#looking for AY RPK and REV info
			if regexp2.match(r) != None:
				#summing LY and HY for each column
				for i in range(0,17):
					deb = r[:3]
					fin = r[-3:].strip()
					self.tableModel.setDataNoDisplayUpdate(VERTICAL_HEADER.index(r),i, float(self.tableModel.getData(VERTICAL_HEADER.index(deb + " HY " + fin),i)) + float(self.tableModel.getData(VERTICAL_HEADER.index(deb + " LY " + fin),i)))


		# 3 - populate yield, lF and RASK
		regexp3 = re.compile("(Yield|LF|RASK).(AY|LY|AY).(?!YoY).*")
		for r in VERTICAL_HEADER:
			# looking for yield LF ans RASK
			if regexp3.match(r):
				# calcul des yields
				if r[:5]=="Yield":
					#verif de division par 0
					fin = r[5:]
					for i in range(0,17):
						if  self.tableModel.getDataFloat(VERTICAL_HEADER.index("RPK" + r[5:]),i) > 0:
							self.tableModel.setDataNoDisplayUpdate(VERTICAL_HEADER.index(r),i, self.tableModel.getDataFloat(VERTICAL_HEADER.index("Rev" + fin),i) /  self.tableModel.getDataFloat(VERTICAL_HEADER.index("RPK" + fin ),i))
				#calculation LF
				# if r[:2] == "LF":
					# for i in range(0,17):
						# if  self.tableModel.getDataFloat(VERTICAL_HEADER.index("ASK" + r[2:]),i) > 0:
							# self.tableModel.setDataNoDisplayUpdate(VERTICAL_HEADER.index(r),i, self.tableModel.getDataFloat(VERTICAL_HEADER.index("RPK" + fin),i) /  self.tableModel.getDataFloat(VERTICAL_HEADER.index("ASK" + fin ),i))

				#calculation RASK


		# 4 - calculate YoY for ASK/RPK/Yield/Rev
		# -------------------

		regexp = re.compile("(RPK|Yield|Rev).(AY|LY|HY).(YoY).*")
		for r in VERTICAL_HEADER:
			# looking for all YoY except LF
			if regexp.match(r):
				prefix = r[:-3].strip()
				for i in range(0,17):
					if  self.tableModel.getDataFloat(VERTICAL_HEADER.index(prefix+" Ref"),i)> 0:
						self.tableModel.setDataNoDisplayUpdate(VERTICAL_HEADER.index(r), i, str((self.tableModel.getDataFloat(VERTICAL_HEADER.index(prefix+" CY"),i) /  self.tableModel.getDataFloat(VERTICAL_HEADER.index(prefix+" Ref"),i) - 1) * 100 )+ "%")
						# if self.debug == True:
							# print(r + ": " + str(self.tableData[VERTICAL_HEADER.index(prefix+" CY")][i]))
							# print (r + " :" + str(self.tableData[VERTICAL_HEADER.index(prefix+" CY")][i] /  self.tableData[VERTICAL_HEADER.index(prefix+" Ref")][i] - 1) * 100 + "%")

		# 5 - calculate CY-PY for LF
		# --------------------------

	def updateDisplay(self):
		""" update the display of this tabs """
		print("Display should be updated ")

	def cell_clicked_event(self, index):

		#for debuggin purpose only
		print("Cell r:" + str(index.row()) + " ,c:" + str(index.column()) + " clicked - Value :" + index.data(Qt.DisplayRole).toString() + " " +str(self.tableModel.arraydata[index.row()][index.column()]))

		#determine if the clicked cell what kind of data is it and if it is editable or not
		# RPK or yield are the only editable cells


		#open pop up window
		header = VERTICAL_HEADER[index.row()]
		regexp = re.compile("(RPK|Yield).*")
		if regexp.match(header) and index.column() < 12:
			Window_modif(self, index)
			#pass

	def center(self):

		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
