"""
备份脚本 - 保存当前所有关键文件的状态
日期: 2025-12-23
"""
import paramiko
from scp import SCPClient
import os
from datetime import datetime

host = "43.130.229.184"
user = "root"
pw = "baifan100100"
remote_base = "/root/soeasyhub_v2"

# 创建备份目录
backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(backup_dir, exist_ok=True)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=pw)

files_to_backup = [
    'templates/index.html',
    'templates/tools/index.html',
    'templates/tools/detail.html',
    'routes/tools.py',
    'routes/blog.py',
    'app.py'
]

with SCPClient(ssh.get_transport()) as scp:
    for file in files_to_backup:
        try:
            remote_path = f'{remote_base}/{file}'
            local_path = f'{backup_dir}/{file.replace("/", "_")}'
            scp.get(remote_path, local_path)
            print(f"✓ Backed up: {file}")
        except Exception as e:
            print(f"✗ Failed to backup {file}: {e}")

print(f"\n✅ Backup completed in: {backup_dir}")
ssh.close()
