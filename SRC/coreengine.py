from static import *
from database import *

# Core engine for handling data for budget
# =========================================

class Core():

	def __init__(self, database, debug=True):

		self.debug = debug
	
		# the core is based on
		# --------------------
		# - DATA for forecasting
			# 3 type of data * 5 traffic flow * 3 yld * 17 months (12+ 1 year + 4 quarters)
		self.DATA_FCST = [[[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18]],[[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18]],[[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18]]]		
		# - reference DATA
		self.DATA_REF = [[[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18]],[[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18]],[[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18],[[0]*18,[0]*18,[0]*18]]]
		
		
		# - events lists (FIFO)
		self.events_list = []
		# - type of treatment
		self.treatment = NON_RETREATMENT
		# - a database to get & store data
		self.db = database
		# - a reference table
		self.referenceTable = "DATA_REF_0"
		# - the dictionnary of reference table
		self.referenceDict = self.db.fetch_architecture()
		
		# count numberOfRoutes
		self.countNumberOfRoutes()



	# getting data
	# ------------

	def set_treatment(treatment):
		""" specify which treatment will be done on the data """
		self.treatment = treatment


	def get_data_CY(self):
		self.db.populate_table(self.DATA_FCST, self.db.get_data_CY())

	def get_data_ref(self):
		if self.treatment == RETREATMENT:
			self.db.populate_table(self.DATA_REF, self.db.get_data_ref_rt(self.referenceTable))
		else:
			self.db.populate_table(self.DATA_REF, self.db.get_data_ref_nrt(self.referenceTable))
		#print("Data for May Rev Local LY" + str(self.DATA_REF[ARRAY_DATA.index("Rev")][ARRAY_FLOW.index("Local")][ARRAY_YIELD.index("LY")][5]))
		
	# ###############
	# handling data
	# ##############

	# scope of treatment
	# -----------------

	def countNumberOfRoutes(self):
		self.numberOfRoutes = self.db.countNumberOfRoutes()


	def set_rfs_used(self, rfs):
		""" add to the db that we are handling a specific route """
		self.db.set_rfs_used(rfs)

	def clear_rfs_used(self):
		""" clear the list of the rfs handled in the db """
		if self.debug == True:
			print("Clearing RFS used table")
		self.db.clear_rfs_used()

	def setRef(self, ref):
		""" set reference table according to its nickname and retrieve data"""
		self.referenceTable = self.referenceDict[ref]
		if self.debug == True:
			print("New reference table set to " + self.referenceTable)
		self.get_data_ref()

	# Event handling
	# --------------

	def add_event(self, ev):
		self.events_list.append(ev)

	def __events_handler(self):
		# take an event and apply what is needed
		res = 0
		
		for e in self.events_list:
		# for each event handle it and then remove it
			res = e.handle(self)
			self.events_list.pop(0)
		return res
			
	def process_events(self):
		#apply all pending change
		res = self.__events_handler()
		#retrieve new data
		self.get_data_CY()
		#flag to make sure process is OK
		return res
		# clearing the list
		self.clear_events()
		
	def clear_events(self):
		self.events_list = []

