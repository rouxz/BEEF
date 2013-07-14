import database
import os
from static import *
from sqlite3 import *

db =  DBPATH_UNIX + "/" + DBNAME_UNIX

try:
	print("Platform different than windows / switching to SQLite")
	print(db)
	cnx = connect( db)
	print("Connection to db " + db + " successfull")
except:
	print("Connection to db " + db + " failed")