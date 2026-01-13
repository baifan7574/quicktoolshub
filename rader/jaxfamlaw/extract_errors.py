import sqlite3
import json

db_path = r'C:\Users\bai\.n8n\database.sqlite'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # 获取最新的 2 条执行数据
    cursor.execute("SELECT executionId, data FROM execution_data ORDER BY executionId DESC LIMIT 2")
    rows = cursor.fetchall()
    
    for eid, data_json in rows:
        print(f"\n--- Execution ID: {eid} ---")
        data = json.loads(data_json)
        if 'resultData' in data and 'runData' in data['resultData']:
            run_data = data['resultData']['runData']
            for node_name, history in run_data.items():
                print(f"Node: {node_name}")
                for entry in history:
                    if 'error' in entry:
                        print(f"  Error message: {entry['error'].get('message')}")
                        print(f"  Error stack: {entry['error'].get('stack')}")
        else:
            print("No runData found.")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
