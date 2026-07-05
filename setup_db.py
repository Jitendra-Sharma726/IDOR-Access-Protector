import sqlite3
import os 

DB_FILE = 'users.db'

def setup():
  if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create tables
cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
cursor.execute('CREATE TABLE documents (doc_id INTEGER PRIMARY KEY, owner_id INTEGER, title TEXT, content TEXT)')

# Inject the Attacker (User ID: 1001) and their document (Doc ID: 55)
cursor.execute("INSERT INTO Users VALUES (1001, 'hacker', 'hacker123')")
cursor.execute("INSERT INTO documents VALUES (55, 1001, 'January Statement', 'Account Balance: $10.00. No recent transcations.')")

#Inject the Victim (User ID: 1089) and their private document (DOC ID: 56)
cursor.execute("INSERT INTO users VALUES (1089, 'alice', 'alice123')")
cursor.execute("INSERT INTO documents VALUES (56, 1089, 'offShore Account Details', 'Routing: 987654321 | Balance : $2,500, 000.00 | Location : Cayman Islands')")

conn.commit()
conn.close()


print("Database 'users.db' initialized.")
print("Seeded Hacker (Doc 55) and Alice (Doc 56).")

if __name__ == "__main__":
  setup()
  
