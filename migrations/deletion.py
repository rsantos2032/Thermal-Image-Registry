import sqlite3

path = "api/database/app.db"
conn = sqlite3.connect(path)
cursor = conn.cursor()

# Just meant to reset the DB for testing

cursor.execute('''DROP TABLE log_information''')
conn.commit()
conn.close()