# STATIC DATA

# shared parameters
# ----------------
equivData = {"Rev": 0, "RPK": 1, "ASK": 2}
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