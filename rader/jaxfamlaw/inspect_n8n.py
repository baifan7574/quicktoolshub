import sqlite3
import json

db_path = r'C:\Users\bai\.n8n\database.sqlite'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT nodes, connections FROM workflow_entity WHERE name = 'Gemini GitHub Updater'")
    row = cursor.fetchone()
    
    if row:
        nodes = json.loads(row[0])
        connections = json.loads(row[1])
        print("--- NODES ---")
        for n in nodes:
            print(f"Name: {n.get('name')}, ID: {n.get('id')}, Type: {n.get('type')}")
        print("\n--- CONNECTIONS ---")
        print(json.dumps(connections, indent=2))
    conn.close()
except Exception as e:
    print(f"Error: {e}")
