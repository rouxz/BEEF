import pygal
from pygal.style import LightStyle
from static import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtSvg import *
import sys
from PyQt4.QtWebKit import QGraphicsWebView
from mainGui import *
import re


#######################################
#
#	Widget for Handling SVG			 #
#
#######################################


class WidgetChart2(QSvgWidget):

	def __init__(self, parent):
		"""create the widget"""
		QSvgWidget.__init__(self, parent)

		# fetching the chart
		# ==================

		# file to open
		self.file = "bar_chart.svg"
		if sys.platform == "linux2":
			self.directorySep = "/"
		else:
			self.directorySep = "\\"
		self.wd = os.getcwd()



		# displaying the chart
		# ====================

		# self.svg_widget = QSvgWidget(self)
		self.load(self.wd + self.directorySep + self.file)




class WidgetChart(QWidget):
	""" a widget displaying a chart stock as a svg in the local file """

	def __init__(self, parent):
		"""create the widget"""
		QWidget.__init__(self, parent)

		# fetching the chart
		# ==================

		# file to open
		self.file = "bar_chart.svg"
		if sys.platform == "linux2":
			self.directorySep = "/"
		else:
			self.directorySep = "\\"
		self.wd = os.getcwd()



		# displaying the chart
		# ====================

		# scene for displaying the graphics
		self.scene = QGraphicsScene()
		# view widget where the graphics will be
		self.view = QGraphicsView(self.scene)

		#get the size of the svg
		self.br = QGraphicsSvgItem(self.wd + self.directorySep + self.file).boundingRect()

		# web that is to say the svg file
		self.webview = QGraphicsWebView()
		self.loadWidget()


		# add the chart in the scene
		self.scene.addItem(self.webview)
		# resize the view
		self.view.resize(self.br.width()+10, self.br.height()+10)

		#add the view to the parent layout
		self.setLayout(QVBoxLayout())
		self.layout().addWidget(self.view)
		
	def loadWidget(self):
		self.webview.load(QUrl(self.wd + self.directorySep + self.file))
		self.webview.setFlags(QGraphicsItem.ItemClipsToShape)
		# self.webview.setCacheMode(QGraphicsItem.NoCache)
		self.webview.resize(self.br.width(), self.br.height())



class QuarterSplitSvgCreator():
	""" generate a chart for KPI split per quarter ASK / RPK / yield / RASK """
	def __init__(self, data):
	
		# bar_chart = pygal.Bar(style=LightStyle)
		bar_chart = pygal.Bar(fill=True, style=LightStyle,  label_font_size=12, major_label_font_size=14)
		
		# abscisses
		bar_chart.x_labels = ["Q1","Q2", "Q3","Q4","Annual"]# Then create a bar graph object
		bar_chart.x_labels_major = ["Annual"]
		
		# add data into the chart
		bar_chart.add("ASK", data[0])
		bar_chart.add("RPK",  data[1])
		bar_chart.add("Yield",  data[2])
		
		
		#render the file
		bar_chart.render_to_file('bar_chart2.svg')

if __name__ == "__main__":

	QuarterSplitSvgCreator([[0.2, -0.3, 0, 0.5, 0.25],[0.2, -0.3, 0, 0.5, 0.25],[0.2, -0.3, 0, 0.5, 0.25]])
	app = QApplication(sys.argv)
	w = WidgetChart(None)
	# topwindow of the gui
	w.show()
	sys.exit(app.exec_())