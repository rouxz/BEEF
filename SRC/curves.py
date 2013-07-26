import static as STATIC
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from table_gui import *
import re
# for plotting
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

import random

class Curves(QDialog):
	""" windows to modif values with a tableView """

	# def __init__(self, parent, table_view, index, debug = True):
	def __init__(self, parent, debug = True):
		QDialog.__init__(self, parent)

		self.debug = debug

		# self.table_view = table_view
		# self.index = index


		#set the UI
		self.initUI()


		#launch the UI
		self.exec_()




	def initUI(self):
		""" display the window properly """

		#global layout for the widget
		self.layout = QGridLayout()

		# figure of the curses
		self.plot = plt.figure()
		# Qwidget to have the plot
		self.canvas = FigureCanvas(self.plot)

		self.drawPlot()


		# title insertion in the layout
		self.layout.addWidget(QLabel("Title"), 0,0)

		# the chart
		self.layout.addWidget(self.canvas, 0,1)

		#setting the main layout
		self.setLayout(self.layout)

		self.setWindowTitle("My curves")
		self.show()

	def drawPlot(self):
		# random data
		data = [random.random() for i in range(15)]
		data2 = [random.random() for i in range(15)]

        # axis
		self.axData = self.plot.add_subplot(211)
		self.axYoY = self.plot.add_subplot(212)

		# discards the old graph
		self.axData.hold(False)
		self.axYoY.hold(False)

		# plot data
		#self.axData.plot(STATIC.TABLE_TITLE[:12],data, '*-',STATIC.TABLE_TITLE[:12],data2, '*-')
		self.axData.

# for testing
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Curves(None)
    main.show()
    sys.exit(app.exec_())