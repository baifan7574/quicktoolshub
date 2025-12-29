"""
简单统计 if/endif
"""
import paramiko
from scp import SCPClient

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)

with SCPClient(ssh.get_transport()) as scp:
    scp.get('/root/soeasyhub_v2/templates/tools/detail.html', 'detail_server.html')

with open('detail_server.html', 'r', encoding='utf-8') as f:
    content = f.read()

if_count = content.count('{%if') + content.count('{% if')
endif_count = content.count('{% endif %}')

print("if 数量:", if_count)
print("endif 数量:", endif_count)
print("缺少:", if_count - endif_count)

# 找到最后几个 if/endif
lines = content.split('\n')
print("\n最后 20 个 if/elif/endif:")
count = 0
for i in range(len(lines)-1, -1, -1):
    if '{% if' in lines[i] or '{% elif' in lines[i] or '{% endif %}' in lines[i]:
        print(f"行 {i+1}: {lines[i].strip()}")
        count += 1
        if count >= 20:
            break

ssh.close()
