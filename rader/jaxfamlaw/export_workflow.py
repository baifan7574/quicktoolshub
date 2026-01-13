import sqlite3
import json
import os

db_path = r"C:\Users\bai\.n8n\database.sqlite"
workflow_name = "Gemini GitHub Updater"

if not os.path.exists(db_path):
    print(f"Error: Database not found at {db_path}")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT nodes, connections FROM workflow_entity WHERE name = ?;", (workflow_name,))
    row = cursor.fetchone()
    
    if row:
        nodes = json.loads(row[0])
        connections = json.loads(row[1])
        workflow_data = {
            "name": workflow_name,
            "nodes": nodes,
            "connections": connections
        }
        print(json.dumps(workflow_data, indent=2))
    else:
        print(f"Error: Workflow '{workflow_name}' not found.")
        
    conn.close()
except Exception as e:
    print(f"Database error: {e}")
