import sqlite3
import json

db_path = r'C:\Users\bai\.n8n\database.sqlite'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nodes FROM workflow_entity WHERE name = 'Gemini GitHub Updater'")
    row = cursor.fetchone()
    
    if row:
        w_id, nodes_json = row
        nodes = json.loads(nodes_json)
        
        # 1. 更新节点参数 (使用 .bat 启动器)
        for node in nodes:
            if node['name'] == 'Write To G-Drive (Local)':
                node['parameters']['command'] = r'd:\quicktoolshub\雷达监控。\GRICH\launch_sync.bat "{{$json.content}}"'
        
        # 2. 串联连接 (Webhook -> GitHub -> G-Drive)
        # Webhook: fdd9cb57-99a4-4c27-8b95-a3652353b72c
        # GitHub: d569e958-4375-461b-9b60-df758064f352
        # G-Drive: gd-sync-node-id
        new_connections = {
            "Webhook": {
                "main": [[{"node": "GitHub", "type": "main", "index": 0}]]
            },
            "GitHub": {
                "main": [[{"node": "Write To G-Drive (Local)", "type": "main", "index": 0}]]
            }
        }
        
        cursor.execute("UPDATE workflow_entity SET nodes = ?, connections = ?, active = 1 WHERE id = ?", 
                       (json.dumps(nodes), json.dumps(new_connections), w_id))
        conn.commit()
        print("Workflow chained and launcher set.")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
