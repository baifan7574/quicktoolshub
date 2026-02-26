from supabase import create_client
import os
import json

config = {}
with open('.agent/Token..txt', 'r', encoding='utf-8') as f:
    for line in f:
        if 'Project URL:' in line: config['url'] = line.split('URL:')[1].strip()
        if 'Secret keys:' in line: config['key'] = line.split('keys:')[1].strip()

sb = create_client(config['url'], config['key'])

# Fetch exactly 10 slugs that have articles
res = sb.table('grich_keywords_pool').select('slug').not_.is_('final_article', 'null').limit(10).execute()

print(f"--- FOUD ARTICLES ---")
for r in res.data:
    print(f"- {r['slug']}")
