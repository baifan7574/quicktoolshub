import sqlite3
import json
import os

db_path = r"C:\Users\bai\.n8n\database.sqlite"

if not os.path.exists(db_path):
    print(f"Error: Database not found at {db_path}")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, type FROM credentials_entity;")
    rows = cursor.fetchall()
    
    print("Available credentials:")
    for row in rows:
        print(f"- Name: {row[0]}, Type: {row[1]}")
        
    conn.close()
except Exception as e:
    print(f"Database error: {e}")
