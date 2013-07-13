import database
import os
from static import *

try:
			
	if self.platform == PLATFORM_WINDOWS:
		#connection MS ACCESS
		self.cnx = connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=" + DBPATH + "\\" + dbname + ";Uid=Admin;Pwd=;")
	else:
		# Connection to sqlite3
		print("Platform different than windows / switching to SQLite")
		print(DBPATH_UNIX + "/" + DBNAME_UNIX)
		self.cnx = sqlite3.connect(os.getcwd() + "/" + DBPATH_UNIX + "/" + DBNAME_UNIX)
			
	print("Connection to db " + DBNAME_UNIX + " successfull")
	# clear RFS used for consistency purpose
	self.clear_rfs_used()
	
except:
	print("Connection to db " + os.getcwd() + "/" + DBPATH_UNIX + "/" + DBNAME_UNIX + " failed")