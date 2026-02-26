import os
import re
import requests
from supabase import create_client, Client

# Path to Token file
TOKEN_FILE = os.path.join(".agent", "Token..txt")

def parse_token_file():
    config = {}
    if not os.path.exists(TOKEN_FILE):
        print(f"Error: {TOKEN_FILE} not found.")
        return config
    
    with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            if "Project URL:" in line:
                config['url'] = line.split("Project URL:")[1].strip()
            if "Secret keys:" in line:
                config['key'] = line.split("Secret keys:")[1].strip()
            if "Project ID:" in line:
                config['project_ref'] = line.split("Project ID:")[1].strip()
            if "api令牌" in line:
                # Handle full width colon if present or standard
                parts = line.split("：") if "：" in line else line.split(":")
                if len(parts) > 1:
                    config['pat'] = parts[1].strip()
    return config

def check_table(supabase: Client):
    try:
        # Try to select from the table. If it doesn't exist, it should raise an error.
        supabase.table("grich_keywords_pool").select("*").limit(1).execute()
        return True
    except Exception as e:
        # Using a broad exception catch because specific API error might vary
        if "relation" in str(e) and "does not exist" in str(e):
            return False
        # If specific PostgrestError: {'code': '42P01', 'details': None, 'hint': None, 'message': 'relation "public.grich_keywords_pool" does not exist'}
        # We can also check the message text
        print(f"Check table exception: {e}")
        return False

def create_table_via_api(config):
    ref = config.get('project_ref')
    pat = config.get('pat')
    
    if not ref or not pat:
        print("Missing Project Ref or PAT to create table.")
        return False

    url = f"https://api.supabase.com/v1/projects/{ref}/sql"
    headers = {
        "Authorization": f"Bearer {pat}",
        "Content-Type": "application/json"
    }
    
    sql = """
    CREATE TABLE IF NOT EXISTS grich_keywords_pool (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        keyword TEXT,
        slug TEXT UNIQUE,
        category TEXT,
        color_tag TEXT,
        state TEXT,
        is_downloaded BOOLEAN DEFAULT false,
        is_refined BOOLEAN DEFAULT false,
        last_mined_at TIMESTAMP WITH TIME ZONE
    );
    CREATE INDEX IF NOT EXISTS idx_grich_keywords_slug ON grich_keywords_pool(slug);
    """
    
    payload = {"query": sql}
    
    print(f"Executing SQL via Management API on project {ref}...")
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 201 or response.status_code == 200:
        print("Table creation SQL executed successfully.")
        return True
    else:
        print(f"Failed to create table: {response.status_code} - {response.text}")
        return False

def main():
    print("Reading configuration...")
    config = parse_token_file()
    
    if 'url' not in config or 'key' not in config:
        print("Failed to find Supabase URL or Secret Key in Token..txt")
        return

    print(f"Connecting to Supabase: {config['url']}")
    supabase: Client = create_client(config['url'], config['key'])
    
    print("Checking if 'grich_keywords_pool' exists...")
    if check_table(supabase):
        print("Table 'grich_keywords_pool' already exists.")
    else:
        print("Table does not exist. Attempting to create...")
        if create_table_via_api(config):
            print("Verifying creation...")
            if check_table(supabase):
                print("Table 'grich_keywords_pool' is ready.")
            else:
                print("Error: SQL executed but table still not found.")
        else:
            print("Could not create table. Please create it manually.")

if __name__ == "__main__":
    main()
