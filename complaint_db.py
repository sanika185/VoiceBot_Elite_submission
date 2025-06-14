import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user_name TEXT,
            complaint_text TEXT,
            department TEXT,
            status TEXT DEFAULT 'Pending'
        )
    ''')
    conn.commit()
    conn.close()

def store_complaint(user_name, complaint_text, department):
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO complaints (timestamp, user_name, complaint_text, department) 
        VALUES (?, ?, ?, ?)
    ''', (datetime.now().isoformat(), user_name, complaint_text, department))
    conn.commit()
    conn.close()
