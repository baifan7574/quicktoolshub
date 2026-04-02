import os
import requests
import json

TOKEN_FILE = os.path.join(".agent", "Token..txt")

def parse_token_file():
    config = {}
    with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if "Project ID:" in line:
                config['ref'] = line.split("Project ID:")[1].strip()
            if "api令牌" in line:
                parts = line.split("：") if "：" in line else line.split(":")
                if len(parts) > 1:
                    config['pat'] = parts[1].strip()
    return config

def main():
    config = parse_token_file()
    ref = config.get('ref')
    pat = config.get('pat')
    
    if not ref or not pat:
        print("❌ Missing Project Ref or PAT.")
        return

    # Supabase Management API to run SQL
    url = f"https://api.supabase.com/v1/projects/{ref}/query" 
    # Note: endpoint might be /sql or /query depending on version. 
    # init_grich_db used /sql which is for the CLI/Management content?
    # Let's try /query first if that's standard for Psql via API?
    # Actually, the official Management API is https://api.supabase.com/v1
    # POST /v1/projects/{ref}/query
    
    headers = {
        "Authorization": f"Bearer {pat}",
        "Content-Type": "application/json"
    }
    
    sql = "ALTER TABLE grich_keywords_pool ADD COLUMN IF NOT EXISTS content_json JSONB;"
    payload = {"query": sql}
    
    print(f"🔌 Parsing SQL to {url}...")
    res = requests.post(url, json=payload, headers=headers)
    
    if res.status_code == 200: # or 201
         print("✅ SQL Executed Successfully.")
         print(res.json())
    elif res.status_code == 404:
         # Try /sql endpoint if /query failed
         print("⚠️ /query endpoint not found, trying /sql...")
         url2 = f"https://api.supabase.com/v1/projects/{ref}/sql"
         res2 = requests.post(url2, json=payload, headers=headers)
         if res2.status_code in [200, 201]:
             print("✅ SQL Executed Successfully via /sql.")
         else:
             print(f"❌ Failed via /sql: {res2.status_code} {res2.text}")
    else:
         print(f"❌ Failed: {res.status_code} {res.text}")

if __name__ == "__main__":
    main()
