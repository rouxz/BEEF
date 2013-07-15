try:
	from pyodbc import *
except ImportError:
	from sqlite3 import *
from static import *

class Database():
	def __init__(self, platform=PLATFORM_WINDOWS, debug=True):
		# Connect to an access database using pyodbc

		self.debug = debug
		self.platform = platform

		if self.platform == PLATFORM_WINDOWS:
			self.dbname = DBNAME
		else:
			self.dbname = DBNAME_UNIX

		
		try:

			if self.platform == PLATFORM_WINDOWS:
				#connection MS ACCESS
				self.cnx = connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=" + DBPATH + "\\" + self.dbname + ";Uid=Admin;Pwd=;")
			else:
				# Connection to sqlite3
				print("Platform different than windows / switching to SQLite")
				self.cnx = connect(DBPATH_UNIX + "/" + self.dbname)

			print("Connection to db " + self.dbname + " successfull")
			# clear RFS used for consistency purpose
			self.clear_rfs_used()
		except:
			print("Connection to db " + self.dbname + " failed")


	def __del__(self):
		#disconnect properly from database
		try:
			self.cnx.close()
			print("Connection to database " + self.dbname + " closed")
		except:
			pass

	def __execute_query(self, query):
		"""retrieve values within db """
		try:
			cursor = self.cnx.cursor()
			#execute the SQL change
			if self.debug == True:
				print("Executing following SQL command : " + query + "on db :" + self.dbname)
			lines = cursor.execute(query)
			data = cursor.fetchall()
			return data
		except:
			if self.debug == True:
				print("Error executing : " + query + " on db :" + self.dbname)
			return "Error"


	def __commit_query(self, SQLquery):
		""" Commiting change a SQL query"""
		try:
			cursor = self.cnx.cursor()
			#execute the SQL change
			if self.debug == True:
				print("Executing following SQL command : " + SQLquery + " on db : " + self.dbname)
			cursor.execute(SQLquery)
			#commit change in db
			self.cnx.commit()
			return 0
		except:
			self.cnx.rollback()
			if self.debug == True:
				print("Error executing : " + SQLquery + " on db : " + self.dbname)
			return 1




	###################################
	# structure of db
	##################################

	def fetch_architecture(self):
		""" get all tables that can be used by the programm """
		lst = []
		for chunk in self.__execute_query("SELECT TABLE_NAME, NICK_NAME FROM TABLE_REF WHERE NICK_NAME <> '';"):
			lst.append(chunk)
		return lst

	def clear_rfs_used(self):
		""" clear the list of RFS currently handled """
		if self.platform == PLATFORM_WINDOWS:
			return self.__commit_query("DELETE * FROM RFS_USED;")
		else:
			return self.__commit_query("DELETE FROM RFS_USED;")


	###################################
	# getting data
	###################################

	def get_data_CY(self):
		""" will fetch all data for routes defined in the RFS_USED table """
		if self.platform == PLATFORM_WINDOWS:
			return self.__execute_query("SELECT MONTH, CONTRIB, FLOW, REV, REV_EX_ROX, RPK, ASK FROM R_G_DATA_RAW;")
		else:
			return self.__execute_query("SELECT DATA_RAW.MONTH, DATA_RAW.CONTRIB, DATA_RAW.FLOW, DATA_RAW.REV, DATA_RAW.REV_EX_ROX, DATA_RAW.RPK, DATA_RAW.ASK FROM DATA_RAW INNER JOIN RFS_USED ON DATA_RAW.RFS = RFS_USED.RFS GROUP BY DATA_RAW.MONTH, DATA_RAW.CONTRIB, DATA_RAW.FLOW;")

	def get_data_ref_nrt(self, ref):
		""" get data for the reference non retreated"""
		query = "SELECT " + ref + ".MONTH, " + ref + ".CONTRIB, " + ref + ".FLOW, Sum(" + ref + ".REV) AS REV, Sum(" + ref + ".REV_EX_ROX) AS REV_EX_ROX, Sum(" + ref + ".RPK) AS RPK, Sum(" + ref + ".ASK) AS ASK FROM " + ref + " INNER JOIN RFS_USED ON " + ref + ".RFS = RFS_USED.RFS GROUP BY " + ref + ".MONTH, " + ref + ".CONTRIB, " + ref + ".FLOW;"
		return self.__execute_query(query)

	def get_data_ref_rt(self, ref):
		""" get data for the reference retreated"""
		query = "SELECT " + ref + ".MONTH, " + ref + ".CONTRIB, " + ref + ".FLOW, Sum(" + ref + ".REV) AS REV, Sum(" + ref + ".REV_EX_ROX) AS REV_EX_ROX, Sum(" + ref + ".RPK) AS RPK, Sum(" + ref + ".ASK) AS ASK FROM (RFS_USED INNER JOIN RFS_RETRAITEMENT ON RFS_USED.RFS = RFS_RETRAITEMENT.RFS) INNER JOIN " + ref + " ON (RFS_RETRAITEMENT.MONTH = " + ref + ".MONTH) AND (RFS_RETRAITEMENT.RFS_RT = " + ref + ".RFS) GROUP BY " + ref + ".MONTH, " + ref + ".CONTRIB, " + ref + ".FLOW;"
		return self.__execute_query(query)

	def populate_table(self, table, values):
		""" populate a table with the provided values """
		for value in values:
			#print (str(value.MONTH) + " " + value.FLOW + " " + value.CONTRIB + " ")
			# rev ex rox
			table[equivData["Rev"]][equivFlow[value.FLOW]][equivYield[value.CONTRIB]][value.MONTH] = value.REV_EX_ROX
			# rpk
			table[equivData["RPK"]][equivFlow[value.FLOW]][equivYield[value.CONTRIB]][value.MONTH] = value.RPK
			# ask
			table[equivData["ASK"]][equivFlow[value.FLOW]][equivYield[value.CONTRIB]][value.MONTH] = value.ASK

	###################################
	# setting data
	###################################

	def set_rfs_used(self,rfs):
		""" add a rfs in the list of routes to be handled"""
		return self.__commit_query("INSERT INTO RFS_USED (RFS) VALUES ('" + rfs + "');")

	def set_data_percentage(self, type, flow, yld, month, percentage):
		""" modify data within table according to provided percentage """
		if type == "Rev":
			self.__commit_query("UPDATE DATA_RAW SET REV_EX_ROX = REV_EX_ROX * " + str(percentage) + " WHERE DATA_RAW.RFS IN (SELECT RFS FROM RFS_USED);")
		elif type == "RPK":
			self.__commit_query("UPDATE DATA_RAW SET RPK = RPK * " + str(percentage) + " WHERE DATA_RAW.RFS IN (SELECT RFS FROM RFS_USED);")
		else:
			pass

	def set_data_value(self, type, flow, yld, month, value):
		""" modify data within table according to provided value"""
		""" can only be used when one route is selected """
		if type == "Rev":
			self.__commit_query("UPDATE DATA_RAW SET REV_EX_ROX = " + str(percentage) + " WHERE DATA_RAW.RFS IN (SELECT RFS FROM RFS_USED);")
		elif type == "RPK":
			self.__commit_query("UPDATE DATA_RAW SET RPK = " + str(percentage) + " WHERE DATA_RAW.RFS IN (SELECT RFS FROM RFS_USED);")
		else:
			pass

