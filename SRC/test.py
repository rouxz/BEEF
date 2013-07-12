# testting all the modules

from database import *
from static import *
from coreengine import *

import re

#regexp = re.compile("(Rev|RPK).*(?!YoY)$")
reg = "(Rev|RPK).AY.(?!YoY).*"
regexp = re.compile(reg)
test = "RPK AY YoY"
print(test + " " + str(regexp.match(test)))

