import sqlite3
db_path = r'C:\Users\bai\.n8n\database.sqlite'
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT startedAt, status FROM execution_entity ORDER BY startedAt DESC LIMIT 3")
    rows = cursor.fetchall()
    print("Latest Executions:")
    for r in rows:
        print(r)
    conn.close()
except Exception as e:
    print(f"Error: {e}")
