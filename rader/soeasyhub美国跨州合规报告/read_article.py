import os
import textwrap
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

# Check article for the first slug
slug = "does-a-california-rn-license-transfer-to-other-states"

print(f"📖 Reading Final Article for: {slug}...\n")

try:
    res = supabase.table("grich_keywords_pool")\
        .select("final_article")\
        .eq("slug", slug)\
        .single()\
        .execute()
    
    if res.data and res.data.get('final_article'):
        article = res.data['final_article']
        print("-" * 50)
        # Print first ~1500 chars to show structure
        print(textwrap.shorten(article, width=1500, placeholder="...\n[Continued]"))
        print("-" * 50)
        print(f"\n✅ Total Length: {len(article)} chars")
    else:
        print("❌ Article still null or not found.")

except Exception as e:
    print(f"❌ Error: {e}")
