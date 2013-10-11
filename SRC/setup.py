from distutils.core import setup
import py2exe 



py2exe_opciones = {'py2exe': {"includes":["sip", "decimal"]}}
script = [{"script":"main.py", "icon_resources": [(1, "beef2.ico")]}]

setup(windows=script,options=py2exe_opciones)
#setup(console=['main.py'])