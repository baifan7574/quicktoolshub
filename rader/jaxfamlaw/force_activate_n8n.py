import sqlite3
import os

db_path = r"C:\Users\bai\.n8n\database.sqlite"

if not os.path.exists(db_path):
    print(f"Error: Database not found at {db_path}")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if workflow exists and get current status
    cursor.execute("SELECT name, active FROM workflow_entity WHERE name = 'Gemini GitHub Updater';")
    row = cursor.fetchone()
    if row:
        print(f"Found workflow: {row[0]}, Active: {row[1]}")
        cursor.execute("UPDATE workflow_entity SET active = 1 WHERE name = 'Gemini GitHub Updater';")
        conn.commit()
        print(f"Update successful. Rows affected: {cursor.rowcount}")
    else:
        print("Error: Workflow 'Gemini GitHub Updater' not found in database.")
        # Let's list all workflows to help debugging
        cursor.execute("SELECT name, active FROM workflow_entity;")
        rows = cursor.fetchall()
        print("Available workflows:")
        for r in rows:
            print(f"- {r[0]} (Active: {r[1]})")
            
    conn.close()
except Exception as e:
    print(f"Database error: {e}")
