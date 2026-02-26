import os
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
BUCKET = "raw-handbooks"

print(f"📂 Listing files in bucket: '{BUCKET}'...")

try:
    # List all files in the root of the bucket
    res = supabase.storage.from_(BUCKET).list()
    
    if not res:
        print("⚠️ Bucket appears empty or list returned nothing.")
    else:
        print(f"✅ Found {len(res)} files:")
        for file in res:
            print(f"   - {file['name']} (Size: {file.get('metadata', {}).get('size', 'Unknown')} bytes)")

except Exception as e:
    print(f"❌ Error listing bucket: {e}")
