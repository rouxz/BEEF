# testting all the modules

from database import *
from static import *
from coreengine import *

print("Test")

db = Database(DBNAME)
core = Core(db)
core.set_rfs_used("FAA")

core.get_data_CY()
print(core.referenceList)
db.__del__()