import static as STATIC
import os
import file_manager

try:
	from pyodbc import *
except ImportError:
	from sqlite3 import *

# retirer
from param import *

class RemoteServer():

	def __init__(self, database, params, debug=True):
		""" connect local database to remote one """
		self.debug = debug
		self.platform = params.system

		try:

			#get address of database
			self.remote_db = params.remote_db_address

			if self.platform == STATIC.PLATFORM_WINDOWS:
				#connection MS ACCESS
				print("Connecting to : " + self.remote_db)
				self.cnx = connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=" +  self.remote_db.replace("\\", "\\\\") + ";Uid=Admin;Pwd=;")
			else:
				# Connection to sqlite3
				print("Platform different than windows / no remote connection")
				return -1

			print("Connection to remote db " + self.remote_db + " successfull")

		except:
			print("Connection to db " + self.remote_db + " failed")



	def importRemoteData(self, database):
		""" import all data from remote data to local db """
        #clear data within locale db
		#import all remote dataw
		pass

if __name__ == "__main__":
	p = DynamicParameters(True)
	RemoteServer(None, p, True)