
import os
from supabase import create_client

TOKEN_FILE = os.path.join(".agent", "Token..txt")

def load_config():
    config = {
        'url': os.getenv('SUPABASE_URL'),
        'key': os.getenv('SUPABASE_KEY'),
    }
    if not config['url'] or not config['key']:
        try:
            with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    if "Project URL:" in line: config['url'] = line.split("URL:")[1].strip()
                    if "Secret keys:" in line: config['key'] = line.split("keys:")[1].strip()
        except:
            pass
    return config

config = load_config()
supabase = create_client(config['url'], config['key'])

# Check for recently updated PDFs
# Since we don't have a clear "updated_at" for pdf_url change specifically, we can just list some pdf_urls
# and see if they look new (based on filename timestamp)

print("Fetching recent PDF URLs...")
res = supabase.table("grich_keywords_pool")\
    .select("slug, pdf_url")\
    .eq("is_refined", True)\
    .neq("pdf_url", "null")\
    .limit(10)\
    .execute()

for r in res.data:
    print(f"{r['slug']}: {r['pdf_url']}")
