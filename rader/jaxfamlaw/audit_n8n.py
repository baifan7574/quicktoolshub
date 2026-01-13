import sqlite3
import json

db_path = r'C:\Users\bai\.n8n\database.sqlite'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, nodes, connections FROM workflow_entity")
    rows = cursor.fetchall()
    for name, nodes_json, conn_json in rows:
        print(f"\n=== Workflow: {name} ===")
        nodes = json.loads(nodes_json)
        connections = json.loads(conn_json)
        
        print("  Nodes:")
        for n in nodes:
            print(f"    - [{n.get('id')}] {n.get('name')} ({n.get('type')})")
            if n.get('name') == 'Write To G-Drive (Local)':
                print(f"      Command: {n.get('parameters', {}).get('command')}")
        
        print("  Connections:")
        print(json.dumps(connections, indent=4))
    conn.close()
except Exception as e:
    print(f"Error: {e}")
