from supabase import create_client
import os

config = {}
with open('.agent/Token..txt', 'r', encoding='utf-8') as f:
    for line in f:
        if 'Project URL:' in line: config['url'] = line.split('URL:')[1].strip()
        if 'Secret keys:' in line: config['key'] = line.split('keys:')[1].strip()

sb = create_client(config['url'], config['key'])

# List logic
res = sb.storage.from_('raw-handbooks').list(options={'limit': 200})
res.sort(key=lambda x: x.get('created_at', ''), reverse=True)

print(f"--- STORAGE AUDIT ---")
print(f"Total Files in Storage: {len(res)}")
print(f"Top 10 Most Recent Files:")
for f in res[:10]:
    print(f"- {f['name']} | Created: {f['created_at']}")
