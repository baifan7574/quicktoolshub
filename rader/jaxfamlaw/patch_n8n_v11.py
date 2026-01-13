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
        
        temp_file = r'd:\quicktoolshub\雷达监控。\GRICH\temp_n8n_sync.txt'
        py_path = r'C:\Users\bai\AppData\Local\Programs\Python\Python311\python.exe'
        script_path = r'd:\quicktoolshub\雷达监控。\GRICH\append_to_gdrive.py'
        repo_dir = r'd:\quicktoolshub\雷达监控。\GRICH\grich-astro'

        # 我们重建节点列表，确保逻辑最简化
        new_nodes = [
            # 1. Webhook
            {
                "parameters": {"httpMethod": "POST", "path": "gemini-update", "options": {}},
                "name": "Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [100, 300],
                "id": "node-webhook-id"
            },
            # 2. GitHub Sync (Local Git Command - Bulletproof)
            {
                "parameters": {
                    "command": f'powershell -Command "cd \'{repo_dir}\'; Set-Content -Path \'{{{{$json.body.path}}}}\' -Value @\'\\n{{{{$json.body.content}}}}\\n\'@; git add . ; git commit -m \'{{{{$json.body.message}}}}\'; git push"'
                },
                "name": "Git Sync (Local)",
                "type": "n8n-nodes-base.executeCommand",
                "typeVersion": 1,
                "position": [350, 200],
                "id": "node-git-sync-id"
            },
            # 3. G-Drive Memory (Local Sync - Bulletproof)
            {
                "parameters": {
                    "command": f'powershell -Command "Set-Content -Path \'{temp_file}\' -Value @\'\\n{{{{$json.body.content}}}}\\n\'@; & \'{py_path}\' \'{script_path}\' \'{temp_file}\'"'
                },
                "name": "Write To G-Drive (Local)",
                "type": "n8n-nodes-base.executeCommand",
                "typeVersion": 1,
                "position": [350, 400],
                "id": "node-gdrive-sync-id"
            }
        ]

        # 串联连线：Webhook -> Git -> G-Drive (串联可以保证出错时易于排查，且避免并发冲突)
        new_connections = {
            "Webhook": {
                "main": [[{"node": "Git Sync (Local)", "type": "main", "index": 0}]]
            },
            "Git Sync (Local)": {
                "main": [[{"node": "Write To G-Drive (Local)", "type": "main", "index": 0}]]
            }
        }

        cursor.execute("UPDATE workflow_entity SET nodes = ?, connections = ?, active = 1 WHERE id = ?", 
                       (json.dumps(new_nodes), json.dumps(new_connections), workflow_id))
        conn.commit()
        print("Database V11 (Serial Git) patch applied.")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
