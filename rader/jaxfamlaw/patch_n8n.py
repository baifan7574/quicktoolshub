import sqlite3
import json

db_path = r'C:\Users\bai\.n8n\database.sqlite'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 获取当前工作流
    cursor.execute("SELECT id, nodes FROM workflow_entity WHERE name = 'Gemini GitHub Updater'")
    row = cursor.fetchone()

    if not row:
        print("Error: Workflow not found")
        conn.close()
        exit(1)

    workflow_id, nodes_json = row
    nodes = json.loads(nodes_json)

    # 修改 Execute Command 节点
    for node in nodes:
        if node['name'] == 'Write To G-Drive (Local)':
            # 使用最简单的命令，去除复杂的 cmd /c 和重定向
            node['parameters']['command'] = r'python "d:\quicktoolshub\雷达监控。\GRICH\append_to_gdrive.py" "{{$json.body.content}}"'
            print("Updated node command.")

    new_nodes_json = json.dumps(nodes)
    cursor.execute("UPDATE workflow_entity SET nodes = ? WHERE id = ?", (new_nodes_json, workflow_id))
    conn.commit()
    print("Database updated successfully.")
    conn.close()

except Exception as e:
    print(f"Error: {e}")
