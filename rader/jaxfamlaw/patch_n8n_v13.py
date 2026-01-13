import sqlite3
import json

db_path = r'C:\Users\bai\.n8n\database.sqlite'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nodes FROM workflow_entity WHERE name = 'Gemini GitHub Updater'")
    row = cursor.fetchone()

    if row:
        workflow_id, nodes_json = row
        nodes = json.loads(nodes_json)
        
        py_path = r'C:\Users\bai\AppData\Local\Programs\Python\Python311\python.exe'
        sync_script = r'd:\quicktoolshub\雷达监控。\GRICH\super_sync.py'
        payload_file = r'd:\quicktoolshub\雷达监控。\GRICH\auto_payload.json'

        # V13: 使用 PowerShell 将 JSON 写入文件，然后再由 Python 读取
        new_nodes = [
            {
                "parameters": {"httpMethod": "POST", "path": "gemini-update", "options": {}},
                "name": "Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [100, 300],
                "id": "node-webhook-v13"
            },
            {
                "parameters": {
                    # 使用 Set-Content 写入文件，然后运行 Python
                    "command": f'powershell -Command "Set-Content -Path \'{payload_file}\' -Value \'{{{{JSON.stringify($json.body)}}}}\'; & \'{py_path}\' \'{sync_script}\' \'{payload_file}\'"'
                },
                "name": "Super Sync Driver",
                "type": "n8n-nodes-base.executeCommand",
                "typeVersion": 1,
                "position": [400, 300],
                "id": "node-super-sync-v13"
            }
        ]

        new_connections = {
            "Webhook": {
                "main": [[{"node": "Super Sync Driver", "type": "main", "index": 0}]]
            }
        }

        cursor.execute("UPDATE workflow_entity SET nodes = ?, connections = ?, active = 1 WHERE id = ?", 
                       (json.dumps(new_nodes), json.dumps(new_connections), workflow_id))
        conn.commit()
        print("Database V13 (File Handoff) patch applied.")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
