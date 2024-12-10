import sqlite3
import os

path = "api/database/app.db"
conn = sqlite3.connect(path)
cursor = conn.cursor()

# Just meant to reset the DB for testing

cursor.execute('''DROP TABLE log_information''')
conn.commit()
conn.close()

path = "api/uploads/"
for file in os.listdir(path):
    file_path = os.path.join(path, file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print("Failed to delete %s. Reason: %s" % (file_path, e))
        
print("Deletion Completed.")