from supabase import create_client, Client
import os

TOKEN_FILE = os.path.join(".agent", "Token..txt")

def _load_config():
    config = {}
    with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if "Project URL:" in line: config['url'] = line.split("URL:")[1].strip()
            if "Secret keys:" in line: config['key'] = line.split("keys:")[1].strip()
    return config

def add_column():
    config = _load_config()
    supabase: Client = create_client(config['url'], config['key'])
    # We use a dummy update to a non-existent field to see if it works, or we can use the 'rpc' method if the user has an 'exec_sql' rpc.
    # Since most Supabase setups don't have exec_sql by default, and I can't use the SQL editor directly:
    print("🚀 PLEASE EXECUTE THIS IN SUPABASE SQL EDITOR:")
    print("ALTER TABLE grich_keywords_pool ADD COLUMN IF NOT EXISTS pdf_url TEXT;")

if __name__ == "__main__":
    add_column()
