from static import *

# define an event on the database
# -------------------------------

class Event():
	
	__type = None
	
	
	def __init__(self):
		pass
	
	def handle(self, core):
		""" class used to process an event """
		return 0
		

class EventModifValue(Event):
	""" send to coreengine the new value we want to apply """
	
	
	def __init__(self, valueRev, valueRPK, month, yld, flow):
		Event.__init__(self)
		self.type = MODIFICATION
		self.month = month
		self.yld = yld
		self.flow = flow
		self.valueRev = valueRev
		self.valueRPK = valueRPK
		
	def handle(self, core):
		#Event.handle(core);
		# calculate the % of modif versus the data
		percentageRev = self.valueRev / core.DATA_FCST[equivData["Rev"]][equivFlow[self.flow]][ARRAY_YIELD.index(self.yld)][self.month]
		percentageRPK = self.valueRPK / core.DATA_FCST[equivData["Rev"]][equivFlow[self.flow]][ARRAY_YIELD.index(self.yld)][self.month]
		# commit these data into the db
		res1 = core.db.set_data_percentage("Rev", self.flow, self.yld, self.month, percentageRev)
		res2 = core.db.set_data_percentage("RPK", self.flow, self.yld, self.month, percentageRPK)
		#results of the commit
		return (res1 + res2)
		
class EventModifScope(Event):
	""" define a new scope ie add a new route with the route scope """
	
	__month = None
	__yld = None
	__flow = None
	__valueRev = None
	__valueRPK = None
	
	def __init__(self, rfs):
		Event.__init__(self)
	
		
	def handle(self, core):
		Event.handle(core);
		

class EventAddAbsoluteData(Event):
	""" class for sending a specific value for one single route in the database """
	
	def __init__(self, valueRev, valueRPK, month, yld, flow):
		Event.__init__(self)
		self.type = ABSOLUTE
		self.month = month
		self.yld = yld
		self.flow = flow
		self.valueRev = valueRev
		self.valueRPK = valueRPK
		
	def handle(self, core):
		res1 = core.db.set_data_value(self.flow, self.yld, self.month, self.valueRev, self.valueRPK)
		return res1 