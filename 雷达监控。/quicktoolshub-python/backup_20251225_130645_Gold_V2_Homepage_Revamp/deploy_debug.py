"""
Deploy Debug tools.py
"""
import paramiko
from scp import SCPClient
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)

with SCPClient(ssh.get_transport()) as scp:
    scp.put('tools_debug.py', '/root/soeasyhub_v2/routes/tools.py')
    print("✅ Uploaded debug version")

print("Restarting...")
ssh.exec_command("pkill -9 gunicorn || true")
time.sleep(2)
ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
time.sleep(5)

# Check logs immediately
stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn")
print(stdout.read().decode())

ssh.close()
