import psycopg2
import os

TOKEN_FILE = os.path.join(".agent", "Token..txt")

def get_config():
    config = {}
    with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if "Project ID:" in line:
                config['project_ref'] = line.split("Project ID:")[1].strip()
            if "Secret keys:" in line:
                config['key'] = line.split("Secret keys:")[1].strip()
    return config

def main():
    config = get_config()
    db_pass = config.get('key')
    project_ref = config.get('project_ref')
    
    conn_str = f"postgres://postgres:{db_pass}@db.{project_ref}.supabase.co:5432/postgres"
    print(f"Connecting to: {conn_str.replace(db_pass, '***')}")
    
    try:
        conn = psycopg2.connect(conn_str, connect_timeout=10)
        cur = conn.cursor()
        
        # Add column final_article
        alter_sql = "ALTER TABLE grich_keywords_pool ADD COLUMN IF NOT EXISTS final_article TEXT;"
        cur.execute(alter_sql)
        conn.commit()
        print("✅ Column 'final_article' added successfully.")
        conn.close()
    except Exception as e:
        print(f"❌ Connection/Migration failed: {e}")

if __name__ == "__main__":
    main()
