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
    
    # Try different connection string patterns
    conn_str = f"postgres://postgres:{db_pass}@db.{project_ref}.supabase.co:5432/postgres"

    print(f"Connecting to add pdf_url column...")
    
    try:
        conn = psycopg2.connect(conn_str, connect_timeout=5)
        cur = conn.cursor()
        
        # Add column
        alter_sql = "ALTER TABLE grich_keywords_pool ADD COLUMN IF NOT EXISTS pdf_url TEXT;"
        cur.execute(alter_sql)
        conn.commit()
        print("✅ Column pdf_url added successfully.")
        conn.close()
    except Exception as e:
        print(f"❌ Failed via primary conn: {e}")
        # Try pooler connection
        try:
             conn_str_pooler = f"postgres://postgres.{project_ref}:{db_pass}@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
             conn = psycopg2.connect(conn_str_pooler, connect_timeout=5)
             cur = conn.cursor()
             cur.execute("ALTER TABLE grich_keywords_pool ADD COLUMN IF NOT EXISTS pdf_url TEXT;")
             conn.commit()
             print("✅ Column pdf_url added successfully via pooler.")
             conn.close()
        except Exception as e2:
             print(f"❌ Failed via pooler: {e2}")

if __name__ == "__main__":
    main()
