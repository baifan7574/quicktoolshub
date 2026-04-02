import os
import json
from supabase import create_client, Client

# Load config
TOKEN_FILE = os.path.join(".agent", "Token..txt")
config = {}
with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        if "Project URL:" in line:
            config['url'] = line.split("URL:")[1].strip()
        if "Secret keys:" in line:
            config['key'] = line.split("keys:")[1].strip()

supabase: Client = create_client(config['url'], config['key'])

# Target slug that had good data
slug = "does-a-california-rn-license-transfer-to-other-states"

print(f"🔍 Fetching FULL JSON for: {slug}...\n")

try:
    res = supabase.table("grich_keywords_pool")\
        .select("content_json")\
        .eq("slug", slug)\
        .single()\
        .execute()
    
    if res.data and res.data['content_json']:
        # Pretty print the JSON
        print(json.dumps(res.data['content_json'], indent=2, ensure_ascii=False))
    else:
        print("❌ Data not found or content_json is null.")

except Exception as e:
    print(f"❌ Error: {e}")
