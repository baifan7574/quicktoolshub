import sqlite3
import json

db_path = r'C:\Users\bai\.n8n\database.sqlite'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT data FROM credentials_entity WHERE id='7s9yn9S5CKwyoPWp'")
    row = cursor.fetchone()
    if row:
        # Note: the data is encrypted by n8n. I can't easily decrypt it here without the key.
        # However, I can just use the credentials node in n8n.
        # Wait, if I use the "Execute Command" node, I won't have the credentials injected.
        # To avoid decrypted token exposure, I'll stick to a mixed model:
        # Keep GitHub node (but fix it) OR 
        # I can just try to fix the GitHub node parameters in the DB.
        print("Token exists.")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
