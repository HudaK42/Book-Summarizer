import sqlite3

DB_PATH = "data/app.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

with open("utils/init_db.sql", "r") as file:
    sql_script = file.read()
    cur.executescript(sql_script)

conn.commit()
conn.close()

print("Database initialized successfully!")
