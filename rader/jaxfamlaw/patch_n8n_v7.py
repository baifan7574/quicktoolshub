import sqlite3
import json

db_path = r'C:\Users\bai\.n8n\database.sqlite'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 查找工作流
    cursor.execute("SELECT id, nodes FROM workflow_entity WHERE name = 'Gemini GitHub Updater'")
    row = cursor.fetchone()
    
    if row:
        w_id, nodes_json = row
        nodes = json.loads(nodes_json)
        
        # 强制连接设置 (直接在 JSON 里构造)
        connections = {
            "Webhook": {
                "main": [[
                    {"node": "GitHub", "type": "main", "index": 0},
                    {"node": "Write To G-Drive (Local)", "type": "main", "index": 0}
                ]]
            }
        }
        
        # 强制节点配置
        py_path = r'C:\Users\bai\AppData\Local\Programs\Python\Python311\python.exe'
        script_path = r'd:\quicktoolshub\雷达监控。\GRICH\append_to_gdrive.py'
        
        for node in nodes:
            if node['name'] == 'Write To G-Drive (Local)':
                # 使用 echo 管道，配合绝对路径。{{$json.body.content}} 不需要加引号，因为管道会处理。
                # 但为了安全，我们用简单传参测试先，或者坚持 cmd /c echo
                node['parameters']['command'] = f'cmd /c "echo {{$json.body.content}} | \"{py_path}\" \"{script_path}\""'
                print("Updated node with absolute paths.")

        cursor.execute("UPDATE workflow_entity SET nodes = ?, connections = ?, active = 1 WHERE id = ?", 
                       (json.dumps(nodes), json.dumps(connections), w_id))
        conn.commit()
        print("Database V7 patch applied.")
    
    conn.close()
except Exception as e:
    print(f"Error: {e}")
