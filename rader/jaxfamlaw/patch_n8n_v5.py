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
        for node in nodes:
            if node['name'] == 'Write To G-Drive (Local)':
                # 使用最强大的 PowerShell Once 管道模式，彻底解决引号和换行问题
                node['parameters']['command'] = r'powershell -Command "$input | python \"d:\quicktoolshub\雷达监控。\GRICH\append_to_gdrive.py\""'
        
        cursor.execute("UPDATE workflow_entity SET nodes = ? WHERE id = ?", (json.dumps(nodes), workflow_id))
        conn.commit()
    conn.close()
    print("Database patched with Ultimate PS Pipe.")
except Exception as e:
    print(f"Error: {e}")
