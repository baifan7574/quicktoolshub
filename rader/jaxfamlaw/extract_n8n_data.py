import sqlite3
import json

db_path = r'C:\Users\bai\.n8n\database.sqlite'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # 获取最新的执行记录数据
    cursor.execute("SELECT executionId, data FROM execution_data ORDER BY executionId DESC LIMIT 1")
    row = cursor.fetchone()
    
    if row:
        eid, data_json = row
        print(f"Execution ID: {eid}")
        data = json.loads(data_json)
        # 遍历节点执行结果
        if 'resultData' in data and 'runData' in data['resultData']:
            run_data = data['resultData']['runData']
            for node_name, history in run_data.items():
                print(f"Node: {node_name}")
                for entry in history:
                    if 'error' in entry:
                        print(f"  Error: {entry['error']}")
                    if 'data' in entry and 'main' in entry['data']:
                        print(f"  Status: Success")
        else:
            print("No runData found in execution data.")
    else:
        print("No execution records found.")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
