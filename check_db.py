import sqlite3
conn = sqlite3.connect('cnic_database.db')
c = conn.cursor()
c.execute('SELECT * FROM cnic_records')
print(c.fetchall())
conn.close()