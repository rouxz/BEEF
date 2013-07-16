import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

mydata = [[1,2,3],[1,2,3],[1,2,3],[1,2,3],[1,2,3]]
HEADER = ["A", "B","C"]
ROWS = ["1", "2","3", "4", "5"]

class MyTableView(QTableView):
	""" table specialisation of QTableView displaying all the data and calculated KPI fetched from db"""

	def __init__(self, parent):

		QTableView.__init__(self)

		# define the data to be used
		self.tableData = [[0] * 3]*5

		#define dataModel for MVC
		self.tableModel = TableData(self.tableData, ROWS, HEADER)

		#define the model to be used by the table
		self.setModel(self.tableModel)

		# get data from coreengine
		self.retrieveData()

		# set the font
		self.setFont(QFont("Courier New", 8))

		self.connect(self, SIGNAL("doubleClicked(QModelIndex)"), self.cell_clicked_event)


	def retrieveData(self):
		""" get all data from core engine """



		for r in range(len(ROWS)):
			for c in range(len(HEADER)):
				self.tableModel.setDataNoDisplayUpdate(r, c, mydata[r][c])


		# calcultate all totals



		#update display
		self.tableModel.updateDisplay()





	def cell_clicked_event(self, index):

		#for debuggin purpose only
		print("Cell r:" + str(index.row()) + " ,c:" + str(index.column()) + " clicked - Value :" + index.data(Qt.DisplayRole).toString() + " " +str(self.tableModel.arraydata[index.row()][index.column()]))



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
		self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), self.index(0,0), self.index(len(ROWS),len(HEADER)))


def main():



	# for launching the ui
	app = QApplication(sys.argv)
	# topwindow of the gui
	w = QMainWindow()
	l = QHBoxLayout()
	l.addWidget(MyTableView(w))
	w.setCentralWidget(MyTableView(w))


	w.show()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()


