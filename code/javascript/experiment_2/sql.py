import sqlite3

conn = sqlite3.connect('participants.db')

cursor = conn.cursor()

for row in cursor.execute("SELECT * FROM moral_dynamics WHERE datastring!='NULL'"):
	print row
	string = row[16]
	print string.index("data")
	print string[180:]
	print