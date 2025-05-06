import sqlite3
conn = sqlite3.connect("../DB/keys.db")
cursor = conn.cursor()
cursor.execute("SELECT journalist_id FROM journalist_auth")
print(cursor.fetchall())
conn.close()
