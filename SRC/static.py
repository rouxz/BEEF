# STATIC DATA

# shared parameters
# ----------------
equivData = {"Rev": 0, "RPK": 1, "ASK": 2, "yield": 3, "LF": 4}
equivMonth = {"Jan":1, "Feb":2 , "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
equivFlow = { "Local" : 0, "SH-MH" : 1, "MH-MH" : 2,  "MH-LH" : 3, "All" : 4  }
equivYield = { "HY":1, "LY":0, "AY":2}


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
VERTICAL_HEADER = {"ASK HY CY": 0, "ASK HY Ref": 1, "ASK HY YoY": 2, "ASK LY CY": 3,"ASK LY Ref": 4,"ASK LY YoY": 5,"ASK AY CY": 6,"ASK AY Ref": 7, \
		"ASK AY YoY": 8, "RPK HY CY": 9 , "RPK HY Ref" : 10, "RPK HY YoY": 11, "RPK LY CY": 12, "RPK LY Ref": 13, "RPK LY YoY" : 14, \
		"RPK AY CY" : 15, "RPK AY Ref": 16, "RPK AY YoY" : 17, "LF HY CY": 18, "LF HY Ref" : 19, "LF HY CY-Ref": 20, \
		"LF LY CY": 21, "LF LY Ref": 22, "LF LY CY-Ref": 23, "LF AY CY": 24, "LF AY Ref": 25, "LF AY CY-Ref": 26, \
		"Yield HY CY": 27, "Yield HY Ref": 28, "Yield HY YoY": 29, "Yield LY CY": 30, "Yield LY Ref": 31, "Yield LY YoY": 32, \
		"Yield AY CY": 33, "Yield AY Ref": 34, "Yield AY YoY": 35, "Rev HY CY": 36, "Rev HY Ref": 37, "Rev HY YoY": 38}