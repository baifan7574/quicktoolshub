import sqlite3
import json

db_path = r'C:\Users\bai\.n8n\database.sqlite'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # 查询最近的 5 条执行记录，包括错误详情
    cursor.execute("""
        SELECT startedAt, status, workflowId, errorDetails, resultData 
        FROM execution_entity 
        ORDER BY startedAt DESC 
        LIMIT 5
    """)
    rows = cursor.fetchall()
    
    print(f"{'Started At':<25} | {'Status':<10} | {'Error Details'}")
    print("-" * 80)
    for row in rows:
        started, status, wid, err, res = row
        print(f"{started:<25} | {status:<10} | {err if err else 'None'}")
        if res:
            # 尝试解析结果数据看看有没有 stdout/stderr
            try:
                res_json = json.loads(res)
                # 寻找 Execute Command 节点的结果
                print(f"  Result Data: {str(res_json)[:200]}...")
            except:
                pass
    conn.close()
except Exception as e:
    print(f"Error: {e}")
