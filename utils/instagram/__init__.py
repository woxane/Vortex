import sqlite3

_Connection = sqlite3.connect('../database/Vortex.db' , isolation_level = None , check_same_thread = False)
Cursor = _Connection.cursor()
