import sys

from static import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from mainGui import *
from file_manager import *
from window_modif import *
import re



# ###################################
#
#    DATA HANDLING WITHIN THE GUI   #
#
# ###################################

def color(color_dict):
	return QColor(color_dict["r"],color_dict["v"],color_dict["b"])



class Tabs(QTabWidget):
	""" class for defining the tabs including all the tables """



	def __init__(self, core, sidePanel, status, parent):
		QTabWidget.__init__(self, parent)

		self.parentWidget = parent

		#for user interactions
		self.sidePanel = sidePanel

		#list of all the displayed tabs
		self.tabs = []

		i = 0

		# QLocale.setDefault(QLocale.English, QLocale.UnitedStates )

		# add new tabs
		for flow in ARRAY_FLOW:
			if flow != "All":
				editable = True
			else:
				editable = False
			self.tabs.append(MyTableView(editable, core, flow, self.sidePanel, status, self))
			self.addTab(self.tabs[i], flow)
			i = i +1

		self.setUI()

	def setUI(self):
		self.setMinimumSize(800,300)


	def changeRef(self):
		""" change all reference data in the tableviews """
		for tab in self.tabs:
			tab.retrieveDataRefOnly()

	def updateData(self):
		""" update data in all the table views """
		for tab in self.tabs:
			tab.retrieveData()

	def updateTabs(self):
		""" update the data displayed in all the present tabs"""
		for tab in self.tabs:
			tab.updateDisplay()

	def dataConsistency(self):
		""" will make the total of all flows in the tabs total if it is not editable """
		if len(self.tabs) > 1:
			for tab in self.tabs:
				if tab.flow == "All":
					tab.totalForAllFlow(self.tabs)

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
		if index.isValid() and role == Qt.BackgroundRole:
			# colors in the table
			return self.setBackground(index.row(), role)
		elif index.isValid() and role == Qt.DisplayRole:
			header = VERTICAL_HEADER[index.row()]
			regexp_ask_rpk_rev = re.compile("(RPK|ASK|Rev).*")
			regexp_yield = re.compile("(Yield|RASK).*")
			regexp_LF = re.compile("LF.*")
			# if index then send the string representing point or percentage
			if header[-3:] == "YoY":
				return QVariant(QString.number(float(self.arraydata[index.row()][index.column()]),'f',1) + "%")
			elif header[-6:] == "CY-Ref":
				return QVariant(QString.number(float(self.arraydata[index.row()][index.column()]),'f',1) + "pt")
			# if ASK or RPK divide by 1000
			elif regexp_ask_rpk_rev.match(header) != None:
				#return QVariant(QString.number(float(self.arraydata[index.row()][index.column()])/1000,'f',0))
				local = QLocale(QLocale.French, QLocale.France)
				# return QVariant(QString("%L1").arg(round(float(self.arraydata[index.row()][index.column()])/1000)))
				return QVariant(QString(local.toString(float(self.arraydata[index.row()][index.column()])/1000,'f',0)))
			# if yield display in euro cents with 2 digits after point
			elif regexp_yield.match(header) != None:
				return QVariant(QString.number(float(self.arraydata[index.row()][index.column()])*100,'f',2))
			# if LF then display in percentage
			elif regexp_LF.match(header) != None:
				return QVariant(QString.number(float(self.arraydata[index.row()][index.column()])*100,'f',1) + "%")
			else:
				return QVariant(QString.number(float(self.arraydata[index.row()][index.column()]),'f',3))
		else:
			return QVariant()


	def headerData(self, section, orientation, role):
		""" return header for the table model"""
		if orientation == Qt.Vertical and role == Qt.BackgroundRole:
			return self.setBackground(section, role)
		elif orientation == Qt.Vertical and role == Qt.DisplayRole:
			return QVariant(self.vheader[section])
		elif orientation == Qt.Vertical and role == Qt.TextAlignmentRole:
			return Qt.AlignmentFlag(Qt.AlignRight|Qt.AlignVCenter)
		elif orientation == Qt.Vertical and role == Qt.FontRole:
			font = QFont("Verdana",8)
			header = VERTICAL_HEADER[section]
			regexp_ay = re.compile(".*AY.*")
			regexp_index = re.compile(".*(YoY|CY-Ref).*")
			if regexp_index.match(header) != None:
				font.setItalic(True)
				#font.setLetterSpacing(font.PercentageSpacing, 90)
			if  regexp_ay.match(header) != None:
				font.setBold(True)
			return QVariant(font)
		elif orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return QVariant(self.hheader[section])
		else:
			QVariant()



	def setBackground(self, row, role):
		""" Allow to define background of the cells """
		header = VERTICAL_HEADER[row]
		regex_modifiable = re.compile("(RPK|Yield).(HY|LY).*")
		regex_res = re.compile("(LF|RASK).AY.*")
		# modifiable value
		if regex_modifiable.match(header) != None:
			return QBrush(color(COLOR_EDITABLE))
		elif regex_res.match(header) != None:
			return QBrush(color(COLOR_RES))
		else:
			return QVariant()



	def getDataIndex(self, index):
		""" retrieve data within the data container simple way as a string"""
		#return self.qstr2str(self.data(self.index(r, c), Qt.DisplayRole))
		return self.arraydata[index.row()][index.column()]

	def getDataFloat(self, r, c):
		""" retrieve data within the data container simple way as a string"""
		return float(self.arraydata[r][c])



	def setData(self, index, value, role):
		""" change data in the array containing all the required information """
		if index.isValid() and role == Qt.DisplayRole:
			self.arraydata[index.row()][index.column()] = value
			#show to the world the update
			self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
			return True
		else:
			return False


	def setDataNoDisplayUpdate(self, row, col, value):
		"""change data in the data model without updating the gui """
		self.arraydata[row][col] = value

	def updateDisplay(self):
		self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), self.index(0,0), self.index(len(VERTICAL_HEADER),len(TABLE_TITLE)))


	# def index(self, row, col, parent = QModelIndex()):
		# """ redefinition of the index function """
		# return self.createIndex(row, col)

	#converting Qstring to float
	def qstr2str(self, qstr):
		return str(qstr.toString()).strip()

	def flags(self, index):
		if index.isValid():
			return QAbstractTableModel.flags(self, index) | Qt.ItemIsSelectable | Qt.ItemIsEnabled
		else:
			return QAbstractTableModel.flags(self, index)


class MyTableView(QTableView):
	""" table specialisation of QTableView displaying all the data and calculated KPI fetched from db"""

	def __init__(self, editable, core, flow, sidePanel, status, parent, debug = True):

		QTableView.__init__(self)

		# editability of the table
		self.editable = editable

		# status bar
		self.status = status

		#core engine
		self.core = core

		#sidePanel
		self.sidePanel = sidePanel

		#debug parameter
		self.debug = debug

		#flow represented in this table
		self.flow =  flow

		self.parent = parent

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
		self.tableModel = TableData(self.tableData, DISPLAYED_VERTICAL_HEADER, TABLE_TITLE, parent)

		#define the model to be used by the table
		self.setModel(self.tableModel)

		# set the font
		self.setFont(QFont("Courier New", 8))

		# get data from coreengine
		self.retrieveData()

		 # set the minimum size
		self.setMinimumSize(1400, 800)

		# look and feel
		self.lookAndFeel()


		#connecting events
		#-----------------
		#new way
		self.connect(self, SIGNAL("doubleClicked(QModelIndex)"), self.cell_clicked_event)
		self.connect(self, SIGNAL("clicked(QModelIndex)"), self.cell_one_click)


	def lookAndFeel(self):

		# set row height
		for row in xrange(len(VERTICAL_HEADER)):
			self.setRowHeight(row, HEIGHT_ROW)

		for col in xrange(len(TABLE_TITLE)):
			self.setColumnWidth(col, DEFAULT_COLUMN_WIDTH)

		# add color for changeable data
		if self.editable == True:
			for r in xrange(len(VERTICAL_HEADER)):
				for c in xrange(len(TABLE_TITLE)):
					# self.item(r,c).setBackgroundColor(QColor(225, 0, 225))
					pass

		# hide some rows
		regexp_non_necessary = re.compile("(RASK|ASK|LF).(HY|LY).*")
		for row in  VERTICAL_HEADER:
			if regexp_non_necessary.match(row) != None:
				self.hideRow(VERTICAL_HEADER.index(row))

	def getData(self, index):
		return self.tableModel.getData(index.row(), index.column())

	def retrieveData(self):
		""" get all data from core engine """

		
		regexp = re.compile("(Rev|RPK).(HY|LY).(?!YoY).*")
		regexp2 = re.compile("ASK.(HY|LY).(CY|Ref)")

		for r in VERTICAL_HEADER:
			row = VERTICAL_HEADER.index(r)
			res = regexp.match(r)
			res2 = regexp2.match(r)

			for c in xrange(len(TABLE_TITLE)):
			
				if c < 12: #data is a month
					# looking for Rev and RPK and ASK data
					# ------------------------------------
					
					if res != None or res2 != None:
						end = r[-3:].strip()
						yld = ARRAY_YIELD.index(r[4:6].strip())
						type = ARRAY_DATA.index(r[:3].strip())
						
						if res != None:
							flw = ARRAY_FLOW.index(self.flow)
						elif res2!= None:
							flw = ARRAY_FLOW.index("All")
						
						# data is either Rev or RPK for CY or ref or ASK AY
						if end == "CY":
							data = self.core.DATA_FCST[type][flw][yld][c + 1]
						else:
							data = self.core.DATA_REF[type][flw][yld][c + 1]
							
						if data != None and data != "":
							self.tableModel.setDataNoDisplayUpdate(row, c, data)
						else:
							self.tableModel.setDataNoDisplayUpdate(row, c, 0)
					else:
						self.tableModel.setDataNoDisplayUpdate(row, c, 0)
				else:
					self.tableModel.setDataNoDisplayUpdate(row, c, 0)


		# calcultate all totals
		self.setDataConsistency()


		#update display
		self.tableModel.updateDisplay()

		# update global GUI
		self.parent.dataConsistency()

	def retrieveDataRefOnly(self):
		""" get all data from core engine """


		regexp = re.compile("(Rev|RPK).(HY|LY).Ref.*")
		regexp2 = re.compile("(ASK).(HY|LY).Ref.*")

		for r in VERTICAL_HEADER:
			row = VERTICAL_HEADER.index(r)
			res = regexp.match(r)
			res2 = regexp2.match(r)
			if res != None or res2 != None:
				for c in xrange(len(TABLE_TITLE)):
					if c < 12: #data is a month
						# looking for Rev and RPK and ASK data
						# ------------------------------------
				
						end = r[-3:].strip()
						yld = ARRAY_YIELD.index(r[4:6].strip())
						type = ARRAY_DATA.index(r[:3].strip())
						
						if res != None:
							flw = ARRAY_FLOW.index(self.flow)
						elif res2!= None:
							flw = ARRAY_FLOW.index("All")
						
						# data is either Rev or RPK for CY or ref or ASK AY
						if end == "Ref":
							data = self.core.DATA_REF[type][flw][yld][c + 1]
						else:
							data = 0
							
						if data != None and data != "":
							self.tableModel.setDataNoDisplayUpdate(row, c, data)
						else:
							self.tableModel.setDataNoDisplayUpdate(row, c, 0)
					else:
							self.tableModel.setDataNoDisplayUpdate(row, c, 0)
					

		# calcultate all totals
		self.setDataConsistency()


		#update display
		self.tableModel.updateDisplay()

		# update global GUI
		self.parent.dataConsistency()

	def setDataConsistency(self):
		""" allow to calculate links within the array representing the table"""

		regexp1 = re.compile("(Rev|RPK|ASK).(HY|LY).(?!YoY).*")

		# calculation on total per line for relevant lines (RPK, REV, ASK) for HY and LY
		# 1- annual
		# 2- quarters
		for r in VERTICAL_HEADER:
			if regexp1.match(r) != None:
				# annual sum
				sum = 0
				for i in xrange(0,12):
					sum += self.tableModel.getDataFloat(VERTICAL_HEADER.index(r),i)
				self.tableModel.setDataNoDisplayUpdate(VERTICAL_HEADER.index(r), 12, sum)
				# quarterly sum
				for q in ARRAY_QUARTERS:
					sum = 0
					for m in q:
						sum += self.tableModel.getDataFloat(VERTICAL_HEADER.index(r), m - 1)
					self.tableModel.setDataNoDisplayUpdate(VERTICAL_HEADER.index(r), 13 + ARRAY_QUARTERS.index(q), sum)

		# 3 - calculate data for AY RPK and REV and ASK
		regexp2 = re.compile("(Rev|RPK|ASK).AY.(?!YoY).*")
		for r in VERTICAL_HEADER:
			#looking for AY RPK and REV info
			if regexp2.match(r) != None:
				# summing LY and HY for each column
				for i in xrange(0,17):
					deb = r[:3]
					fin = r[-3:].strip()
					self.tableModel.setDataNoDisplayUpdate(VERTICAL_HEADER.index(r),i, self.tableModel.getDataFloat(VERTICAL_HEADER.index(deb + " HY " + fin),i) + self.tableModel.getDataFloat(VERTICAL_HEADER.index(deb + " LY " + fin),i))


		# 3 - populate yield, lF and RASK
		regexp4 = re.compile("(Yield|RASK).(AY|LY|HY).(?!YoY).*")
		for r in VERTICAL_HEADER:
			# looking for yield LF ans RASK
			if regexp4.match(r) != None:
				# calcul des yields
				if r[:5]=="Yield":
					#verif de division par 0
					fin = r[5:]
					for i in xrange(0,17):
						if  self.tableModel.getDataFloat(VERTICAL_HEADER.index("RPK" + fin),i) > 0:
							self.tableModel.setDataNoDisplayUpdate(VERTICAL_HEADER.index(r),i, self.tableModel.getDataFloat(VERTICAL_HEADER.index("Rev" + fin),i) /  self.tableModel.getDataFloat(VERTICAL_HEADER.index("RPK" + fin ),i))
				# calculation RASK
				if r[:4] == "RASK":
					fin = r[4:]
					for i in xrange(0,17):
						if  self.tableModel.getDataFloat(VERTICAL_HEADER.index("ASK" + fin),i) > 0:
							self.tableModel.setDataNoDisplayUpdate(VERTICAL_HEADER.index(r),i, self.tableModel.getDataFloat(VERTICAL_HEADER.index("Rev" + fin),i) /  self.tableModel.getDataFloat(VERTICAL_HEADER.index("ASK" + fin ),i))

		# 4 - calcul LF
		# -------------
		regexp5 = re.compile("LF.(AY|LY|HY).(?!CY-Ref).*")
		for r in VERTICAL_HEADER:
			# looking for yield LF ans RASK
			if regexp5.match(r) != None:
				fin = r[2:]
				for i in xrange(17):
					if  self.tableModel.getDataFloat(VERTICAL_HEADER.index("ASK" + fin),i) > 0:
						self.tableModel.setDataNoDisplayUpdate(VERTICAL_HEADER.index(r),i, self.tableModel.getDataFloat(VERTICAL_HEADER.index("RPK" + fin),i) /  self.tableModel.getDataFloat(VERTICAL_HEADER.index("ASK" + fin ),i))




		# 6 - calculate YoY for ASK/RPK/Yield/Rev
		# ---------------------------------------

		regexp6 = re.compile("(RPK|Yield|Rev|RASK|ASK).(AY|LY|HY).(YoY).*")
		for r in VERTICAL_HEADER:
			# looking for all YoY except LF
			if regexp6.match(r) != None:
				prefix = r[:-3].strip()
				for i in xrange(17):
					if  self.tableModel.getDataFloat(VERTICAL_HEADER.index(prefix+" Ref"),i)> 0:
						self.tableModel.setDataNoDisplayUpdate(VERTICAL_HEADER.index(r), i, (self.tableModel.getDataFloat(VERTICAL_HEADER.index(prefix+" CY"),i) /  self.tableModel.getDataFloat(VERTICAL_HEADER.index(prefix+" Ref"),i) - 1) * 100)


		# 7 - calculate CY-PY for LF
		# --------------------------
		regexp7 = re.compile("LF.(HY|LY|AY).CY-Ref")
		for r in VERTICAL_HEADER:
			#looking for LF delta
			if regexp7.match(r) != None:
				prefix = r[:-6].strip()
				for i in xrange(17):
					if self.tableModel.getDataFloat(VERTICAL_HEADER.index(prefix+" Ref"),i) > 0:
						self.tableModel.setDataNoDisplayUpdate(VERTICAL_HEADER.index(r), i, (self.tableModel.getDataFloat(VERTICAL_HEADER.index(prefix+" CY"),i) - self.tableModel.getDataFloat(VERTICAL_HEADER.index(prefix+" Ref"),i) ) * 100)

	
	def totalForAllFlow(self, tabs):
		""" calculate the sum of all tabs whose flow isn't 'All' for a specific table"""
		regexp = re.compile("(Rev|RPK).(HY|LY).(?!YoY).*")

		for r in VERTICAL_HEADER:
			if regexp.match(r) != None:

				for i in xrange(12):
					sum = 0
					for tab in tabs:
						if tab.flow != "All":
							sum += tab.tableModel.getDataFloat(VERTICAL_HEADER.index(r),i)
					self.tableModel.setDataNoDisplayUpdate(VERTICAL_HEADER.index(r), i , sum)

		self.setDataConsistency()
		self.tableModel.updateDisplay()

	def updateDisplay(self):
		""" update the display of this tabs """
		self.tableModel.updateDisplay()
		# for debug purpose
		#print("Display should be updated ")

	def cell_clicked_event(self, index):

		#for debuggin purpose only
		# if self.debug == True:
			# print("Cell r:" + str(index.row()) + " ,c:" + str(index.column()) + " clicked - Value :" + index.getIndex)
		#print("Cell r:" + str(index.row()) + " ,c:" + str(index.column()) + " clicked - Value :" + str(index.data(Qt.DisplayRole).toFloat()) + " " +str(self.tableModel.arraydata[index.row()][index.column()]))

		#determine if the clicked cell what kind of data is it and if it is editable or not
		# RPK or yield are the only editable cells


		#open pop up window
		if self.editable == True:
			header = VERTICAL_HEADER[index.row()]
			regexp = re.compile("(RPK|Yield).(HY|LY).*")
			if regexp.match(header) and index.column() < 12:
				Window_modif(self, index, self.debug)
				#pass


	def cell_one_click(self, index):
		# display message in status bar
		self.status.showMessage("Data: " + VERTICAL_HEADER[index.row()] + " - Month: " + TABLE_TITLE[index.column()] + " Value: " + str(self.tableModel.getDataIndex(index)))


	# def center(self):

		# qr = self.frameGeometry()
		# cp = QDesktopWidget().availableGeometry().center()
		# qr.moveCenter(cp)
		# self.move(qr.topLeft())
