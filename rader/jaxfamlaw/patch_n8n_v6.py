import sqlite3
import json

db_path = r'C:\Users\bai\.n8n\database.sqlite'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 查找指定工作流
    cursor.execute("SELECT id, nodes, connections FROM workflow_entity WHERE name = 'Gemini GitHub Updater'")
    row = cursor.fetchone()
    
    if row:
        w_id, nodes_json, conn_json = row
        nodes = json.loads(nodes_json)
        
        # 1. 修正连接逻辑
        new_connections = {
            "Webhook": {
                "main": [[
                    {"node": "GitHub", "type": "main", "index": 0},
                    {"node": "Write To G-Drive (Local)", "type": "main", "index": 0}
                ]]
            }
        }
        
        # 2. 修正节点内容
        for node in nodes:
            if node['name'] == 'Write To G-Drive (Local)':
                # 使用最稳定的相对路径+管道命令
                node['parameters']['command'] = r'cmd /c "echo {{$json.body.content}} | python .\append_to_gdrive.py"'
        
        # 3. 写入数据库并强制激活
        cursor.execute("UPDATE workflow_entity SET nodes = ?, connections = ?, active = 1 WHERE id = ?", 
                       (json.dumps(nodes), json.dumps(new_connections), w_id))
        conn.commit()
        print(f"Workflow {w_id} patched and activated.")
    else:
        print("Workflow not found.")
    
    conn.close()
except Exception as e:
    print(f"Error: {e}")
