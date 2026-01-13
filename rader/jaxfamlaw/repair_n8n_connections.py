import sqlite3
import json

db_path = r'C:\Users\bai\.n8n\database.sqlite'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nodes, connections FROM workflow_entity WHERE name = 'Gemini GitHub Updater'")
    row = cursor.fetchone()

    if row:
        workflow_id, nodes_json, connections_json = row
        nodes = json.loads(nodes_json)
        connections = json.loads(connections_json)
        
        # 1. 检查连线 (确保 Webhook 同时连到 GitHub 和 G-Drive)
        # Webhook node id: fdd9cb57-99a4-4c27-8b95-a3652353b72c
        # 我们要确保 main[0] 的数组里包含两个节点
        if "Webhook" in connections:
            connections["Webhook"]["main"] = [[
                {"node": "GitHub", "type": "main", "index": 0},
                {"node": "Write To G-Drive (Local)", "type": "main", "index": 0}
            ]]
            print("Fixed node connections.")

        # 2. 检查节点参数 (修正 Python 执行路径)
        for node in nodes:
            if node['name'] == 'Write To G-Drive (Local)':
                # 使用最稳妥的绝对路径，并避免引号冲突
                # 我们不再通过命令行传内容，而是通过 stdin (由之前的 PowerShell 管道实现)
                # 既然之前的测试显示 cmd /c echo | python 有效，我们坚持这个
                node['parameters']['command'] = r'cmd /c "echo {{$json.body.content}} | python d:\quicktoolshub\雷达监控。\GRICH\append_to_gdrive.py"'
                print("Fixed G-Drive node parameters.")

        cursor.execute("UPDATE workflow_entity SET nodes = ?, connections = ?, active = 1 WHERE id = ?", 
                       (json.dumps(nodes), json.dumps(connections), workflow_id))
        conn.commit()
        print("Database patched successfully. Workflow set to ACTIVE.")
    conn.close()
except Exception as e:
    print(f"Error patching database: {e}")
