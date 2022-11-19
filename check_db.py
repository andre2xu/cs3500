import sqlite3

connection = sqlite3.connect('database.db')

cur = connection.cursor()

cur.execute("SELECT * FROM cropdata")

print(cur.fetchall())


connection.close()
