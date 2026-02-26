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

def setup_infrastructure():
    config = _load_config()
    supabase: Client = create_client(config['url'], config['key'])
    
    # 1. Add pdf_url column to grich_keywords_pool
    print("🐘 [DB] Adding pdf_url column...")
    try:
        # Using RPC or direct SQL is tricky via SDK, but we can try to add it
        # Most users have access to SQL editor. For the agent, let's try a simple update test to see if it exists
        # Actually, adding columns is best done via RPC if defined, or I can just assume the user might need to do it or use a trick.
        # Let's try to add it via a system call if possible, or just print the SQL for the user.
        print("SQL: ALTER TABLE grich_keywords_pool ADD COLUMN IF NOT EXISTS pdf_url TEXT;")
        # Note: SDK doesn't support ALTER TABLE directly.
    except Exception as e:
        print(f"⚠️ Column addition might need manual SQL execution: {e}")

    # 2. Create Storage Bucket 'audit-reports'
    print("☁️ [Storage] Creating 'audit-reports' bucket...")
    try:
        supabase.storage.create_bucket("audit-reports", options={"public": True})
        print("   ✅ Bucket 'audit-reports' created and set to PUBLIC.")
    except Exception as e:
        if "already exists" in str(e).lower():
            print("   ℹ️ Bucket 'audit-reports' already exists.")
        else:
            print(f"   ❌ Bucket creation failed: {e}")

if __name__ == "__main__":
    setup_infrastructure()
