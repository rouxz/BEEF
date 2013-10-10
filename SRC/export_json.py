import os
import sys
import codecs

import static as STATIC
from table_gui import *


class Exporter():
	""" class for exporting specific set of data within the table_gui to specific json files """

	def __init__(self, params, tabs):

		self.params = params
		self.wd = os.getcwd()


		#setting repertory serapator
		if self.params.system == "linux2":
			self.directorySep = "/"
		else:
			self.directorySep = "\\"

		self.tabs = tabs


	def export_quarters(self):
		""" data (ASK, RPK, yield ) split per traffic flow """
		if (self.params.debug):
			print("Exporting file : " + "json_flow.json")

		# output file
		outfile = codecs.open(self.wd + self.directorySep + STATIC.PATH_EXPORT + self.directorySep + STATIC.SUBPATH_EXPORT + self.directorySep + "json_flow.json", "w", "utf-8")

		#data for output
		


		# start of file
		outfile.write("[\n")



		for c in xrange(len(STATIC.FLOW_CHARTS)):
			
			# initiate data
			RPK = [0,0,0,0,0]
			ASK = [0,0,0,0,0]
			yld = [0,0,0,0,0]
			
			
			# get data in the tabs models assuming the order of FLOW_CHARTS
			ASK[0] = self.tabs.tabs[STATIC.ARRAY_FLOW.index("All")].model().getDataFloat(STATIC.VERTICAL_HEADER.index("ASK AY YoY"), 12 + c)
			
			for flow in STATIC.ARRAY_FLOW:
				if flow != "All":
					RPK[STATIC.ARRAY_FLOW.index(flow) + 1] = self.tabs.tabs[STATIC.ARRAY_FLOW.index(flow)].model().getDataFloat(STATIC.VERTICAL_HEADER.index("RPK AY YoY"), 12 + c)
					yld[STATIC.ARRAY_FLOW.index(flow) + 1] = self.tabs.tabs[STATIC.ARRAY_FLOW.index(flow)].model().getDataFloat(STATIC.VERTICAL_HEADER.index("Yield AY YoY"), 12 + c)
				else:
					RPK[0] = self.tabs.tabs[STATIC.ARRAY_FLOW.index(flow)].model().getDataFloat(STATIC.VERTICAL_HEADER.index("RPK AY YoY"), 12 + c)
					yld[0] = self.tabs.tabs[STATIC.ARRAY_FLOW.index(flow)].model().getDataFloat(STATIC.VERTICAL_HEADER.index("Yield AY YoY"), 12 + c)

			output = '{ "chart" : "' + STATIC.FLOW_CHARTS[c] +'", "data" : { "RPK" : ['
			# rpk
			for i in xrange(0,4):
				output += str(RPK[i]) 
				if i < 3:
					output += ','
			
			output += '], "yield":[' 
			
			#yield
			for i in xrange(0,4):
				output += str(yld[i]) 
				if i < 3:
					output += ','
			
			output += '], "ASK": [' 
			
			# ASK
			for i in xrange(0,4):
				output += str(ASK[i]) 
				if i < 3:
					output += ','
			
			output += ']} }'
			
			# add a comma or not
			if c < len(STATIC.FLOW_CHARTS)-1:
				output += ',\n'
			else:
				output += '\n'
				
			#writing the line in the file
			outfile.write(output)
		
		

		
		#end of file
		outfile.write("]\n")

		outfile.close()
		if (self.params.debug):
			print("Export done")

	def export_general(self):
		""" export general data (ASK, RPK, yield, RASK) split per quarter """
		if (self.params.debug):
			print("Exporting file : " + "json_quarter.json")

		# output file
		outfile = codecs.open(self.wd + self.directorySep + STATIC.PATH_EXPORT + self.directorySep + STATIC.SUBPATH_EXPORT + self.directorySep + "json_quarter.json", "w", "utf-8")

		#data for output
		


		# start of file
		outfile.write("[\n")

			
		# initiate data
		RPK = [0,0,0,0,0]
		ASK = [0,0,0,0,0]
		RASK = [0,0,0,0,0]
		yld = [0,0,0,0,0]
		
		
		# get data in the tabs models assuming the order of FLOW_CHARTS
		for q in xrange(len(STATIC.QUARTERS)):
			if q < len(STATIC.QUARTERS) - 1:
				c = q + 1
			else:
				c = 0
			
			RPK[q] = self.tabs.tabs[STATIC.ARRAY_FLOW.index("All")].model().getDataFloat(STATIC.VERTICAL_HEADER.index("RPK AY YoY"), 12 + c)
			ASK[q] = self.tabs.tabs[STATIC.ARRAY_FLOW.index("All")].model().getDataFloat(STATIC.VERTICAL_HEADER.index("ASK AY YoY"), 12 + c)
			yld[q] = self.tabs.tabs[STATIC.ARRAY_FLOW.index("All")].model().getDataFloat(STATIC.VERTICAL_HEADER.index("Yield AY YoY"), 12 + c)
			RASK[q] = self.tabs.tabs[STATIC.ARRAY_FLOW.index("All")].model().getDataFloat(STATIC.VERTICAL_HEADER.index("RASK AY YoY"), 12 + c)
			
			

		output = '{ "chart" : "' + STATIC.QUARTER_CHART +'", "data" : { "RPK" : ['
		# rpk
		for i in xrange(len(STATIC.FLOW_CHARTS)):
			output += str(RPK[i]) 
			if i < len(STATIC.QUARTERS) - 1:
				output += ','
		
		output += '], "yield":[' 
		
		#yield
		for i in xrange(len(STATIC.FLOW_CHARTS)):
			output += str(yld[i]) 
			if i < len(STATIC.QUARTERS) - 1:
				output += ','
		
		output += '], "ASK": [' 
		
		# ASK
		for i in xrange(len(STATIC.FLOW_CHARTS)):
			output += str(ASK[i]) 
			if i < len(STATIC.QUARTERS) - 1:
				output += ','
		
		output += '], "RASK": ['
		
		# RASK
		for i in xrange(len(STATIC.FLOW_CHARTS)):
			output += str(RASK[i]) 
			if i < len(STATIC.QUARTERS) - 1:
				output += ','
		
		output += ']} }\n'
		
		# add a comma or not
		# if c < len(STATIC.QUARTERS)-1:
			# output += ',\n'
		# else:
			# output += '\n'
				
		#writing the line in the file
		outfile.write(output)

		
		#end of file
		outfile.write("]\n")

		outfile.close()
		if (self.params.debug):
			print("Export done")



if __name__ == "__main__":
	e = Exporter(DynamicParameters(),None)
	e.export_quarters()