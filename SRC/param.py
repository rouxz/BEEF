import static as STATIC
import os
import file_manager
from os_specifity import *
import re

class DynamicParameters:

	def __init__(self):
		""" read all parameters in a specific file """

		self.system = find_system()


		try:

			#get all parameters
			params = file_manager.readInfo(STATIC.PARAM_FILE, STATIC.PARAM_PATH, STATIC.SPLITER)

			for p in params:
				if p[0] == "remote-database":
					self.remote_db_address = p[1]
					print("Remote db located at " + self.remote_db_address)
				elif p[0] == "debug":
					regexp = re.compile("(OK|True|true|ok|vrai|Vrai|debug|Debug)")
					if regexp.match(p[1]) != None:
						self.debug = True
						print("Debugging mode enabled")
					else:
						self.debug = False
			print("")
			
		except:
			print("Failed to load all the parameters")
			print("")
			
if __name__ == "__main__":
	DynamicParameters(True)