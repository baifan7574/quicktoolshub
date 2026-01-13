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
                # 使用 echo + 管道将内容传给 Python 的 stdin
                # 注意：n8n 的 Execute Command 节点有一个 'executeOnce' 或者可以启用 stdin 输入的选项
                # 但最稳妥的命令是把内容写成一个临时文件。
                # 既然我不想在 n8n 里添加节点，我就用一个单行命令：
                node['parameters']['command'] = r'python "d:\quicktoolshub\雷达监控。\GRICH\append_to_gdrive.py" <<EOF\n{{$json.body.content}}\nEOF'
                # 抱歉，Windows cmd 不支持 <<EOF。
                # 最终方案：直接在 Python 里通过参数传递，但我们只传一句简单的，或者我把 Python 脚本改成去 GitHub 拉取最新的文件内容。
                
                # 等等，n8n 的 Execute Command 节点可以访问之前的节点数据。
                # 我们用 PowerShell 的管道：
                node['parameters']['command'] = r'powershell -Command "$input = @\"\n{{$json.body.content}}\n\"@; $input | python \"d:\quicktoolshub\雷达监控。\GRICH\append_to_gdrive.py\""'
        
        cursor.execute("UPDATE workflow_entity SET nodes = ? WHERE id = ?", (json.dumps(nodes), workflow_id))
        conn.commit()
    conn.close()
    print("Database patched with PowerShell pipe logic.")
except Exception as e:
    print(f"Error: {e}")
