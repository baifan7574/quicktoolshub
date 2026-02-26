from supabase import create_client
import os
import json

config = {}
with open('.agent/Token..txt', 'r', encoding='utf-8') as f:
    for line in f:
        if 'Project URL:' in line: config['url'] = line.split('URL:')[1].strip()
        if 'Secret keys:' in line: config['key'] = line.split('keys:')[1].strip()

sb = create_client(config['url'], config['key'])

# Audit top 5 most recent composed ones
res = sb.table('grich_keywords_pool').select('slug', 'final_article').not_.is_('final_article', 'null').limit(50).execute()
# Filter for ones that were likely just created (they won't have old dates in text or just pick specific slugs we saw in log)
target_slugs = ['florida-medical-reciprocity', 'medical-board-new-york-license-verification', 'illinois-board-of-nursing-reciprocity']

print(f"--- QUALITY AUDIT ---")
for r in res.data:
    if r['slug'] in target_slugs:
        print(f"\n[AUDITING SLUG: {r['slug']}]")
        print(f"Content Length: {len(r['final_article'])} characters")
        has_cta = '<div class="monetization-box"' in r['final_article']
        count_cta = r['final_article'].count('<div class="monetization-box"')
        has_2026 = '2026' in r['final_article']
        print(f"Quality Check: 2026 Mentioned? {has_2026} | CTA Count: {count_cta}")
        print("PREVIEW:")
        print(r['final_article'][:500])
