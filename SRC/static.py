# STATIC DATA

# Global data
# ----------

PROG__SHORT_NAME = "BEEF"
PROG_LONG_NAME = "BEEF"
VERSION = 0.2


# shared parameters
# ----------------
equivData = {"Rev": 0, "RPK": 1, "ASK": 2}
equivMonth = {"Jan":1, "Feb":2 , "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
equivFlow = { "Local" : 0, "SH-MH" : 1, "MH-MH" : 2,  "MH-LH" : 3, "All" : 4  }
equivYield = { "HY":0, "LY":1, "AY":2}
ARRAY_YIELD = ["HY", "LY", "AY"]
ARRAY_FLOW = ["Local", "SH-MH", "MH-MH","MH-LH","All" ]
ARRAY_DATA = ["Rev", "RPK", "ASK"]
ARRAY_QUARTERS = [[1,2,3],[4,5,6],[7,8,9],[10,11,12]]

# for coreengine.py
# ------------
RETREATMENT = "rt"
NON_RETREATMENT ="nrt"


# for event.py
# ------------

# eventType
MODIFICATION = "mod"
COMMIT = "commit"
CHANGE_REF = "change_ref"
GET_DATA ="get_data"

# dataType
YLD = "yld"
RPK = "rpk"

# for database.py
# ---------------
DBNAME = "DATA_PERSO.accdb"
DBPATH = "C:\TOOLS\BEEF\DATA"

# for file_manager.py
# ---------------

HIERARCHY_DIR = "hierarchy"

# for gui.py
# ----------

TITLE_TOPWINDOW = "BEEF - Bugdet Evaluation for Each Flow"

#spacing for top grid layout
GRID_LAYOUT_SPACE = 10

# for table_gui.py
# ----------------

TABLE_TITLE = ["1","2","3","4","5","6","7","8","9","10","11","12","Total","Q1","Q2","Q3","Q4"]


VERTICAL_HEADER = ["ASK HY CY" , "ASK HY Ref" , "ASK HY YoY" , "ASK LY CY" ,"ASK LY Ref" ,"ASK LY YoY" ,"ASK AY CY" ,"ASK AY Ref" , \
		"ASK AY YoY" , "RPK HY CY"  , "RPK HY Ref"  , "RPK HY YoY" , "RPK LY CY" , "RPK LY Ref" , "RPK LY YoY"  , \
		"RPK AY CY"  , "RPK AY Ref" , "RPK AY YoY"  , "LF HY CY" , "LF HY Ref"  , "LF HY CY-Ref" , \
		"LF LY CY" , "LF LY Ref" , "LF LY CY-Ref" , "LF AY CY" , "LF AY Ref" , "LF AY CY-Ref" , \
		"Yield HY CY" , "Yield HY Ref" , "Yield HY YoY" , "Yield LY CY" , "Yield LY Ref" , "Yield LY YoY" , \
		"Yield AY CY" , "Yield AY Ref" , "Yield AY YoY" , "Rev HY CY" , "Rev HY Ref" , "Rev HY YoY" , \
		"Rev LY CY" , "Rev LY Ref" , "Rev LY YoY" , "Rev AY CY" , "Rev AY Ref" , "Rev AY YoY" , \
		"RASK HY CY" , "RASK HY Ref" , "RASK HY YoY" , "RASK LY CY" , "RASK LY Ref" , "RASK LY YoY" , \
		"RASK AY CY" , "RASK AY Ref" , "RASK AY YoY"  ]	
MAX_NUM_LINES = 53