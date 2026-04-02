from supabase import create_client
import os

config = {}
with open('.agent/Token..txt', 'r', encoding='utf-8') as f:
    for line in f:
        if 'Project URL:' in line: config['url'] = line.split('URL:')[1].strip()
        if 'Secret keys:' in line: config['key'] = line.split('keys:')[1].strip()

sb = create_client(config['url'], config['key'])
slug = 'california-nursing-home-administrator-license-reciprocity'
filename = f"{slug}.pdf"

print(f"Downloading {filename} for audit...")
data = sb.storage.from_('raw-handbooks').download(filename)
with open('audit_check.pdf', 'wb') as f:
    f.write(data)
print("File saved as audit_check.pdf")
