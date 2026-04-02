import os
from supabase import create_client

config={}
with open(r'D:\quicktoolshub\rader\美国跨州合规报告\.agent\Token..txt', 'r', encoding='utf-8') as f:
    for line in f:
        if 'Project URL:' in line: config['url'] = line.split('URL:')[1].strip()
        if 'Secret keys:' in line: config['key'] = line.split('keys:')[1].strip()

sb = create_client(config['url'], config['key'])

# Get the most recently uploaded files
files = sb.storage.from_('raw-handbooks').list()
files.sort(key=lambda x: x['created_at'], reverse=True)

for file in files[:3]:
    name = file['name']
    url = sb.storage.from_('raw-handbooks').create_signed_url(name, 3600)
    print(f"File: {name}\nSigned URL: {url['signedURL']}\n")
