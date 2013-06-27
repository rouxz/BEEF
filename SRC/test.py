# testting all the modules

from database import *
from static import *
from coreengine import *

import re

#regexp = re.compile("(Rev|RPK).*(?!YoY)$")
reg = "(Rev|RPK).(HY|LY).(?!YoY).*"
regexp = re.compile(reg)
test = "RPK LY Ref"
print(test + " " + str(regexp.match(test)))

