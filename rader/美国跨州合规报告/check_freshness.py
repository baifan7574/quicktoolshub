from supabase import create_client
import os

config = {}
with open('.agent/Token..txt', 'r', encoding='utf-8') as f:
    for line in f:
        if 'Project URL:' in line: config['url'] = line.split('URL:')[1].strip()
        if 'Secret keys:' in line: config['key'] = line.split('keys:')[1].strip()

sb = create_client(config['url'], config['key'])

# Get the specific record
res = sb.table('grich_keywords_pool').select('*').eq('slug', 'nursing-license-california-lvn').single().execute()
data = res.data

print(f"--- DATABASE AUDIT: {data['slug']} ---")
print(f"Keyword: {data['keyword']}")
print(f"Last Mined At: {data['last_mined_at']} (This is Script 1 seeding time)")
print(f"Is Refined: {data['is_refined']}")
print(f"Article Length: {len(data['final_article'])} characters")
print("\n--- ARTICLE CONTENT PREVIEW (Holy Bible Check) ---")
print(data['final_article'][:1000]) # Show the beginning to check for 2026 mentions
