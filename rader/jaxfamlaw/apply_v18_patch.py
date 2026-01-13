import sqlite3
import json

db_path = r'C:\Users\bai\.n8n\database.sqlite'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 获取工作流
    cursor.execute("SELECT id FROM workflow_entity WHERE name = 'Gemini GitHub Updater'")
    row = cursor.fetchone()
    
    if row:
        workflow_id = row[0]
        
        # 定义 V18 节点 (使用直连模式，避免 shell 干扰)
        nodes = [
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": "gemini-update",
                    "options": {}
                },
                "name": "Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [100, 300],
                "id": "node-webhook-v18"
            },
            {
                "parameters": {
                    "command": "C:\\Users\\bai\\AppData\\Local\\Programs\\Python\\Python311\\python.exe \"d:\\quicktoolshub\\雷达监~1\\GRICH\\super_sync.py\""
                },
                "name": "Super Sync Driver",
                "type": "n8n-nodes-base.executeCommand",
                "id": "node-super-sync-v18",
                "typeVersion": 1,
                "position": [400, 300]
            }
        ]
        
        connections = {
            "Webhook": {
                "main": [[{"node": "Super Sync Driver", "type": "main", "index": 0}]]
            }
        }
        
        cursor.execute('UPDATE workflow_entity SET nodes = ?, connections = ?, active = 1 WHERE id = ?', 
                       (json.dumps(nodes), json.dumps(connections), workflow_id))
        conn.commit()
        print("V18_DB_PATCH_APPLIED")
    else:
        print("WORKFLOW_NOT_FOUND")
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
