import sqlite3
import json

db_path = r'C:\Users\bai\.n8n\database.sqlite'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM workflow_entity WHERE name = 'Gemini GitHub Updater'")
    row = cursor.fetchone()
    
    if row:
        workflow_id = row[0]
        
        # 定义双线并行节点（GitHub + Google Drive）
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
                "id": "webhook-final"
            },
            {
                "parameters": {
                    "resource": "file",
                    "owner": "={{$json.body.owner}}",
                    "repository": "={{$json.body.repo}}",
                    "filePath": "={{ $json.body.path }}",
                    "fileContent": "={{ $json.body.content }}",
                    "commitMessage": "={{ $json.body.message }}"
                },
                "name": "GitHub",
                "type": "n8n-nodes-base.github",
                "typeVersion": 1,
                "position": [350, 200],
                "id": "github-final",
                "credentials": {
                    "githubApi": {
                        "id": "7s9yn9S5CKwyoPWp",
                        "name": "GitHub account"
                    }
                }
            },
            {
                "parameters": {
                    "resource": "file",
                    "operation": "update",
                    "fileId": {
                        "__rl": True,
                        "value": "GRICH_AI_BRAIN/GRICH_MASTER_LOG.md",
                        "mode": "name"
                    },
                    "updateFields": {
                        "appendData": "={{ JSON.stringify($json.body) }}"
                    }
                },
                "name": "Google Drive",
                "type": "n8n-nodes-base.googleDrive",
                "typeVersion": 3,
                "position": [350, 400],
                "id": "gdrive-final"
            }
        ]
        
        # 双线并行连接
        connections = {
            "Webhook": {
                "main": [
                    [
                        {"node": "GitHub", "type": "main", "index": 0},
                        {"node": "Google Drive", "type": "main", "index": 0}
                    ]
                ]
            }
        }
        
        cursor.execute('UPDATE workflow_entity SET nodes = ?, connections = ?, active = 1 WHERE id = ?', 
                       (json.dumps(nodes), json.dumps(connections), workflow_id))
        conn.commit()
        print("DUAL_LINE_PATCH_SUCCESS")
    else:
        print("WORKFLOW_NOT_FOUND")
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
