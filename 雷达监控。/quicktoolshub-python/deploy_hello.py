"""
Deploy Hello World
"""
import paramiko
from scp import SCPClient
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)

print("停止服务...")
ssh.exec_command("pkill -9 gunicorn")
time.sleep(2)

print("上传极简版 tools.py...")
with SCPClient(ssh.get_transport()) as scp:
    scp.put('tools_hello.py', '/root/soeasyhub_v2/routes/tools.py')

print("启动服务...")
cmd = "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
ssh.exec_command(cmd)
time.sleep(5)

# 验证
stdin, stdout, stderr = ssh.exec_command("curl -I http://127.0.0.1:9999/tools/json-formatter")
print(stdout.read().decode())

ssh.close()
