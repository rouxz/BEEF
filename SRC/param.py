import static as STATIC
import os
import file_manager
from os_specifity import *


class DynamicParameters:

	def __init__(self, debug=True):
		""" read all parameters in a specific file """

		self.debug = debug
		self.system = find_system()


		try:

			#get all parameters
			params = file_manager.readInfo(STATIC.PARAM_FILE, STATIC.PARAM_PATH, STATIC.SPLITER)

			for p in params:
				print(p)
				if p[0] == "remote-database":
					self.remote_db_address = p[1]

		except:
			print("Failed to load all the parameters")

if __name__ == "__main__":
	DynamicParameters(True)