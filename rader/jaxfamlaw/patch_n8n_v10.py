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
        
        temp_file = r'd:\quicktoolshub\雷达监控。\GRICH\temp_n8n_sync.txt'
        py_path = r'C:\Users\bai\AppData\Local\Programs\Python\Python311\python.exe'
        script_path = r'd:\quicktoolshub\雷达监控。\GRICH\append_to_gdrive.py'
        
        for node in nodes:
            if node['name'] == 'Write To G-Drive (Local)':
                # 使用 PowerShell Here-String 极其安全地写入临时文件
                # 然后 Python 读取该文件进行追加
                # 注意：n8n 里的变量必须在大括号里
                cmd = f"powershell -Command \"Set-Content -Path '{temp_file}' -Value @'\\n{{{{$json.body.content}}}}\\n'@; & '{py_path}' '{script_path}' '{temp_file}'\""
                node['parameters']['command'] = cmd
                print("Updated node to V10 (Pass-by-File).")

        # 恢复并联连接 (Webhook -> GitHub, Webhook -> G-Drive)
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
        print("Database V10 patch applied successfully.")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
