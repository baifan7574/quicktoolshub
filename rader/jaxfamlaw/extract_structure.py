import sqlite3
import json

db_path = r'C:\Users\bai\.n8n\database.sqlite'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # 获取最近一次成功的执行数据
    cursor.execute("SELECT data FROM execution_data WHERE executionId IN (SELECT id FROM execution_entity WHERE status='success') ORDER BY executionId DESC LIMIT 1")
    row = cursor.fetchone()
    
    if row:
        data = json.loads(row[1])
        # 查看 Webhook 节点的输出
        if 'resultData' in data and 'runData' in data['resultData']:
            webhook_data = data['resultData']['runData'].get('Webhook')
            if webhook_data:
                print("--- Webhook Output Structure ---")
                print(json.dumps(webhook_data[0]['data']['main'][0][0], indent=2))
        else:
            print("No runData found.")
    else:
        print("No successful execution records found to analyze.")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
