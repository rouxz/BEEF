from static import *
from database import *

# Core engine for handling data for budget
# =========================================

class Core():

	def __init__(self, database):

		# the core is based on
		# --------------------
		# - DATA for forecasting
			# 3 type of data * 5 traffic flow * 3 yld * 12 months
		self.DATA_FCST = [[[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13]],[[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13]],[[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13]]]

		# - reference DATA
		self.DATA_REF = [[[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13]],[[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13]],[[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13],[[None]*13,[None]*13,[None]*13]]]
		# - events lists (FIFO)
		self.EVENTS_LIST = []
		# - type of treatment
		self.TREATMENT = NON_RETREATMENT
		# - a database to get & store data
		self.db = database
		# - a reference table
		self.referenceTable = "DATA_REF_0"
		# - the list of reference table
		self.referenceList = self.db.fetch_architecture()



	# getting data
	# ------------

	def set_treatment(treatment):
		""" specify which treatment will be done on the data """
		self.TREATMENT = treatment




	def get_data_CY(self):
		self.db.populate_table(self.DATA_FCST, self.db.get_data_CY())

	def get_data_ref(self):
		if self.TREATMENT == RETREATMENT:
			self.db.populate_table(self.DATA_REF, self.db.get_data_ref_nrt(self.referenceTable))
		else:
			self.db.populate_table(self.DATA_REF, self.db.get_data_ref_rt(self.referenceTable))

	# ###############
	# handling data
	# ##############

	# scope of treatment
	# -----------------

	def set_rfs_used(self, rfs):
		""" define within the db which rfs we are handling """
		self.db.set_rfs_used(rfs)

	def clear_rfs_used(self):
		""" clear the list of the rfs handled in the db """
		self.db.clear_rfs_used()

	def set_ref(self, ref):
		self.referenceTable = ref


	# Event handling
	# --------------

	def add_event(self, ev):
		self.EVENTS_LIST.append(ev)

	def __events_handler(self):
		# take an event and apply what is needed

		for e in self.EVENTS_LIST:
		# for each event handle it and then remove it
			e.handle(self)
			self.EVENTS_LIST.pop(0)

	def save(self):
		#apply all pending change
		self.__events_handler()
		#retrieve new data
		self.get_data_CY()
		

