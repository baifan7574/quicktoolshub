import sqlite3
import json
import os
from datetime import datetime

db_path = r"C:\Users\bai\.n8n\database.sqlite"
workflow_name = "Gemini GitHub Updater"

# 修正：精简引号逻辑，使用 cmd /c 配合 python 全路径
# n8n 会自动处理 {{$json.body.content}}
cmd_template = 'cmd /c ""C:\\Users\\bai\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" "d:\\quicktoolshub\\雷达监控。\\GRICH\\append_to_gdrive.py" "{{$json.body.content}}" >> "d:\\quicktoolshub\\雷达监控。\\GRICH\\n8n_exec.log" 2>&1"'

new_node = {
    "parameters": {
        "command": cmd_template
    },
    "name": "Write To G-Drive (Local)",
    "type": "n8n-nodes-base.executeCommand",
    "typeVersion": 1,
    "position": [
        320,
        480
    ],
    "id": "gd-sync-node-id"
}

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT nodes, connections FROM workflow_entity WHERE name = ?;", (workflow_name,))
    row = cursor.fetchone()
    
    nodes = json.loads(row[0])
    connections = json.loads(row[1])
    
    # 替换现有节点（如果有）
    for i, n in enumerate(nodes):
        if n['name'] == new_node['name']:
            nodes[i] = new_node
            break
    else:
        nodes.append(new_node)
    
    if "Webhook" not in connections:
        connections["Webhook"] = {"main": [[]]}
    
    new_conn = {"node": new_node['name'], "type": "main", "index": 0}
    if new_conn not in connections["Webhook"]["main"][0]:
        connections["Webhook"]["main"][0].append(new_conn)
    
    cursor.execute("UPDATE workflow_entity SET nodes = ?, connections = ?, updatedAt = ?, active = 1 WHERE name = ?;", 
                   (json.dumps(nodes), json.dumps(connections), datetime.now().isoformat(), workflow_name))
    
    conn.commit()
    print("Deployment Fixed & Updated.")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
