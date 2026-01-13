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
        
        # 1. 更新节点参数 (使用系统的 python 路径和 Webhook 节点的变量)
        # 为确保万无一失，我们直接引用 Webhook 节点的输出
        webhook_var = '{{$node["Webhook"].json["body"]["content"]}}'
        py_path = r'C:\Users\bai\AppData\Local\Programs\Python\Python311\python.exe'
        script_path = r'd:\quicktoolshub\雷达监控。\GRICH\append_to_gdrive.py'
        
        for node in nodes:
            if node['name'] == 'Write To G-Drive (Local)':
                # 使用管道模式，直接引用 Webhook 节点
                node['parameters']['command'] = f'cmd /c "echo {webhook_var} | \"{py_path}\" \"{script_path}\""'
        
        # 2. 恢复并联连接 (Webhook -> GitHub & Webhook -> G-Drive)
        new_connections = {
            "Webhook": {
                "main": [
                    [
                        {"node": "GitHub", "type": "main", "index": 0},
                        {"node": "Write To G-Drive (Local)", "type": "main", "index": 0}
                    ]
                ]
            }
        }
        
        cursor.execute("UPDATE workflow_entity SET nodes = ?, connections = ?, active = 1 WHERE id = ?", 
                       (json.dumps(nodes), json.dumps(new_connections), w_id))
        conn.commit()
        print("Workflow patched with parallel fixed mapping.")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
