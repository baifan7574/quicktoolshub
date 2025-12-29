import paramiko
from scp import SCPClient

host = "43.130.229.184"
user = "root"
pw = "baifan100100"
remote_base = "/root/soeasyhub_v2"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=pw)

with SCPClient(ssh.get_transport()) as scp:
    print("Uploading fixed files...")
    scp.put('tools_new.py', f'{remote_base}/routes/tools.py')
    scp.put('blog_final.py', f'{remote_base}/routes/blog.py')
    scp.put('detail_new.html', f'{remote_base}/templates/tools/detail.html')

print("Killing all Gunicorn processes...")
ssh.exec_command('pkill -9 -f gunicorn')

import time
time.sleep(2)

print("Starting Gunicorn on port 9999 (matching Nginx)...")
cmd = f"cd {remote_base} && nohup python3 -m gunicorn -w 4 -b 127.0.0.1:9999 app:app --preload > gunicorn.log 2>&1 &"
ssh.exec_command(cmd)

time.sleep(3)

print("Verifying...")
_, stdout, _ = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
print(stdout.read().decode())

_, stdout, _ = ssh.exec_command("curl -s -o /dev/null -w '%{http_code}' http://localhost:9999/tools/word-counter")
print(f"HTTP Status: {stdout.read().decode()}")

ssh.close()
print("\n✅ Emergency fix deployed!")
