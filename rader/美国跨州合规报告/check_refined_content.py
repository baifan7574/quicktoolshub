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

print("🔍 Inspecting Refined Data (Gold Nuggets)...")

try:
    # Query content_json IS NOT NULL
    # Using 'neq' null check or logical filter
    res = supabase.table("grich_keywords_pool")\
        .select("slug, content_json")\
        .neq("content_json", "null")\
        .limit(5)\
        .execute()
    
    records = res.data
    if not records:
        print("❌ No refined records found in DB.")
    else:
        print(f"✅ Found {len(records)} records with content_json populated:\n")
        for r in records:
            slug = r['slug']
            data = r['content_json']
            print(f"📄 Slug: {slug}")
            # Print simplified structure
            print(f"   💰 Fee: {data.get('application_fee', 'N/A')}")
            print(f"   ⏳ Time: {data.get('processing_time', 'N/A')}")
            # Assuming requirements is list
            reqs = data.get('requirements', [])
            if isinstance(reqs, list):
                 print(f"   📝 Requirements: {len(reqs)} items (e.g. {reqs[0] if reqs else ''}...)")
            else:
                 print(f"   📝 Requirements: {str(reqs)[:50]}...")
            print("-" * 40)

except Exception as e:
    print(f"❌ Verification Failed: {e}")
