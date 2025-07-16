import sqlite3
conn = sqlite3.connect('cnic_database.db')
c = conn.cursor()
c.execute("SELECT * FROM guests")
for row in c.fetchall():
    print(" | ".join(str(col) for col in row))
conn.close()