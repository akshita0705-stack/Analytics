import sqlite3    #python's bulitin database

# connecting to database
conn = sqlite3.connect("events.db")
cursor = conn.cursor()

#This creates table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT,
    user_id INTEGER,
    metadata TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


