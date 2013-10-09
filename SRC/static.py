# STATIC DATA

# Global data
# ----------

PROG_SHORT_NAME = "BEEF"
PROG_LONG_NAME = "BEEF - Budget Estimation for Each Flow"
VERSION = 1.0




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
RETREATMENT = 0
NON_RETREATMENT = 1


# for event.py
# ------------

# eventType
MODIFICATION = 0
ABSOLUTE = 1
COMMIT = 10

CHANGE_REF = 20
GET_DATA = 30

# dataType
YLD = "yld"
RPK = "rpk"

# for database.py
# ---------------
DBNAME = "DATA_PERSO.accdb"
DBPATH = "C:\\Users\\m409577\\Documents\\GitHub\\BEEF\\DATA"
DATA_DIR = "DATA"
DBPATH_UNIX = "DATA"
DBNAME_UNIX = "database_test.db"
PLATFORM_WINDOWS = 1
PLATFORM_LINUX = 2
PLATFORM_MAC = 3


# for param.py
# ------------

PARAM_PATH = "PARAM"
PARAM_FILE = "param.ini"
SPLITER = "="

# for server_connection.py
# ------------------------
DICT_PROFILE = {"IA": "DATA_RAW_IA", "IM": "DATA_RAW_IM", "ID": "DATA_RAW_ID"}


# for file_manager.py
# ---------------

HIERARCHY_DIR = "hierarchy"

# for sideGui.py
# ---------------

PENDING_LABEL = "Pending actions : "

# for gui.py
# ----------

TITLE_TOPWINDOW = "BEEF - Bugdet Evaluation for Each Flow"
TITLE_LINE =      "######################################"

#spacing for top grid layout
GRID_LAYOUT_SPACE = 10

# for table_gui.py
# ----------------

TABLE_TITLE = ["1","2","3","4","5","6","7","8","9","10","11","12","Total","Q1","Q2","Q3","Q4"]
HEIGHT_ROW = 18
DEFAULT_COLUMN_WIDTH = 80


COLOR_EDITABLE = {"r": 150, "v":204, "b": 150}
COLOR_NONEDITABLE = {"r": 204, "v": 255, "b": 204}
COLOR_NONEDITABLE_YOY = {"r": 237, "v": 255, "b": 237}
COLOR_REV = {"r": 255, "v":217, "b": 217}
COLOR_REV_YOY = {"r": 255, "v":240, "b": 240}
COLOR_TOUS_FLUX = {"r": 220, "v":220, "b": 220}
COLOR_TOUS_FLUX_YOY = {"r": 255, "v":255, "b": 255}


VERTICAL_HEADER = ["ASK HY CY" , "ASK HY Ref" , "ASK HY YoY" , "ASK LY CY" ,"ASK LY Ref" ,"ASK LY YoY" ,"ASK AY CY" ,"ASK AY Ref" , \
		"ASK AY YoY" , "RPK HY CY"  , "RPK HY Ref"  , "RPK HY YoY" , "RPK LY CY" , "RPK LY Ref" , "RPK LY YoY"  , \
		"RPK AY CY"  , "RPK AY Ref" , "RPK AY YoY"  , "LF HY CY" , "LF HY Ref"  , "LF HY CY-Ref" , \
		"LF LY CY" , "LF LY Ref" , "LF LY CY-Ref" , "LF AY CY" , "LF AY Ref" , "LF AY CY-Ref" , \
		"Yield HY CY" , "Yield HY Ref" , "Yield HY YoY" , "Yield LY CY" , "Yield LY Ref" , "Yield LY YoY" , \
		"Yield AY CY" , "Yield AY Ref" , "Yield AY YoY" , "Rev HY CY" , "Rev HY Ref" , "Rev HY YoY" , \
		"Rev LY CY" , "Rev LY Ref" , "Rev LY YoY" , "Rev AY CY" , "Rev AY Ref" , "Rev AY YoY" , \
		"RASK HY CY" , "RASK HY Ref" , "RASK HY YoY" , "RASK LY CY" , "RASK LY Ref" , "RASK LY YoY" , \
		"RASK AY CY" , "RASK AY Ref" , "RASK AY YoY"  ]
#DISPLAYED_VERTICAL_HEADER = ["ASK HY CY" , "ASK HY Ref" , "index" , "ASK LY CY" ,"ASK LY Ref" ,"index" ,"ASK CY" ,"ASK Ref" , \
#		"index" , "RPK HY CY"  , "RPK HY Ref"  , "index" , "RPK LY CY" , "RPK LY Ref" , "index"  , \
#		"RPK Total CY"  , "RPK Total Ref" , "index"  , "LF HY CY" , "LF HY Ref"  , "LF HY CY-Ref" , \
#		"LF LY CY" , "LF LY Ref" , "index" , "LF CY" , "LF Ref" , "delta" , \
#		"Yield HY CY" , "Yield HY Ref" , "index" , "Yield LY CY" , "Yield LY Ref" , "index" , \
#		"Yield Total CY" , "Yield Total Ref" , "index" , "Rev HY CY" , "Rev HY Ref" , "index" , \
#		"Rev LY CY" , "Rev LY Ref" , "index" , "Rev Total CY" , "Rev Total Ref" , "index" , \
#		"RASK HY CY" , "RASK HY Ref" , "index" , "RASK LY CY" , "RASK LY Ref" , "index" , \
#		"RASK CY" , "RASK Ref" , "index"  ]

DISPLAYED_VERTICAL_HEADER = ["ASK HY CY" , "ASK HY Ref" , "index" , "ASK LY CY" ,"ASK LY Ref" ,"index" , \
		"CY" , "ASK              Ref" , "index" , \
		"CY" , "RPK HY           Ref" , "index" , \
		"CY" , "RPK LY           Ref" , "index" , \
		"CY" , "RPK Total      Ref" , "index" , \
		"LF HY CY" , "LF HY Ref"  , "LF HY CY-Ref" , "LF LY CY" , "LF LY Ref" , "index" , \
		"CY" , "LF                 Ref" , "delta" , \
		"CY" , "Yield HY          Ref" , "index" , \
		"CY" , "Yield LY          Ref" , "index" , \
		"CY" , "Yield Total    Ref" , "index" , \
		"CY" , "Rev HY           Ref" , "index" , \
		"CY" , "Rev LY           Ref" , "index" , \
		"CY" , "Rev Total      Ref" , "index" , \
		"RASK HY CY" , "RASK HY Ref" , "index" , "RASK LY CY" , "RASK LY Ref" , "index" , \
		"CY" , "RASK             Ref" , "index"  ]

MAX_NUM_LINES = 53


# for modif_window.py
# -------------------

LABEL_CY_RPK = "RPK CY (000)"
LABEL_CY_Yield = "Yield CY (Ects)"
LABEL_REF_RPK = "RPK Ref (000)"
LABEL_REF_Yield = "Yield Ref (Ects)"


# for about.py
# ------------

EXPLANATIONS = "......"
LICENSE_WORDING = "This program is under license :"
LICENSE = "(c) - 2013"

TECHNOLOGY_HEADER = "Program using :"
TECHNOLOGIES_LIST = ["Python v2.6.7", "pyodbc library", "PyQt4", "Mathplotlib"]




