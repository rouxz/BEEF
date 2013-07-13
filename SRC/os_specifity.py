import sys

dictionary_system = { "" : 0, "win32":1, "linux2":2,"darwin":3}

def find_system():
	print("System is " + sys.platform)
	try:
		return dictionary_system[sys.platform]
	except:
		return 0
	