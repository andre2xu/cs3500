import sqlite3
def create_db():
    connection = sqlite3.connect('database.db')
    with open('schema.sql') as f:
        connection.executescript(f.read())
    cur = connection.cursor()
    for i in range (1,11):
        cur.execute(f"INSERT INTO cropdata (plot_num) VALUES({i})")
    connection.commit()
    cur.execute("SELECT * FROM cropdata")
    connection.close()
