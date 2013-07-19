import os
import sys
from static import *

class MyFileManager():
	""" Managing my file """
	def __init__(self, platform=PLATFORM_WINDOWS):
		self.wd = os.getcwd()
		print("")
		print("Working directory is :" + self.wd)
		print("")
	
		#setting repertory serapator
		if platform == PLATFORM_LINUX:
			directorySep = "/"
		else:
			directorySep = "\\"

		#looking for param directory
		self.hierachyDir = self.wd + directorySep + HIERARCHY_DIR
		
		self.listFiles = []
		
		print("changing directory to : " + self.hierachyDir)
		try:
			self.listFiles = os.listdir(self.hierachyDir)
			if len(self.listFiles)>0:
				print("Following hierachy files found :")
			for file in self.listFiles:
				print(file)
			print("")
		except :
			print("Cannot access subdirectory - check installation")


	def getHierarchies(self):
		return self.listFiles

	def getSublines(self, file):
		""" read all lines in a specified file """
		try:
			#setting repertory serapator
			if sys.platform == "linux2":
				directorySep = "/"
			else:
				directorySep = "\\"
			print("Opening : " + self.hierachyDir + directorySep + file)
			fs = open(self.hierachyDir + directorySep + file, 'r')
			sublines = []
			while 1:
				txt = fs.readline()
				if txt == "###":
					break
				else:
					sublines.append(txt[0:3])
			fs.close
			print("Closing : " + self.hierachyDir + directorySep + file)
			#print(sublines)
			return sublines
		except:
			print("Cannot open file : " + file)
			return []


