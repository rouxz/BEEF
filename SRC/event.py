from static import *

# define an event on the database
# -------------------------------

class Event():
	
	__type = None
	
	
	def __init__(self):
		
	
	def handle(self, core):
		""" class used to process an event """
		return 0
		

class EventModifValue(Event):
	""" send to coreengine the new value we want to apply """
	
	__month = None
	__yld = None
	__flow = None
	__valueRev = None
	__valueRPK = None
	
	def __init__(self, valueRev, valueRPK, month, yld, flow):
		Event.__init__(self)
		self.__type = MODIFICATION
		self.__month = month
		self.__yld = yld
		self.__flow = flow
		self.__valueRev = valueRev
		self.__valueRPK = valueRPK
		
	def handle(self, core):
		Event.handle(core);
		# calculate the % of modif versus the data
		percentageRev = self.valueRev / core.DATA_FCST[equivData["Rev"]][equivFlow[self.__flow]][equivYld[self.__yld]][self.__month]
		percentageRPK = self.valueRPK / core.DATA_FCST[equivData["Rev"]][equivFlow[self.__flow]][equivYld[self.__yld]][self.__month]
		# commit these data into the db
		res1 = core.db.set_data_percentage("Rev", self.__flow, self.__yld, self.__month, percentageRev)
		res2 = core.db.set_data_percentage("RPK", self.__flow, self.__yld, self.__month, percentageRev)
		#results of the commit
		return res1 +res 2
		
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
		
