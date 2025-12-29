import paramiko
from scp import SCPClient
import os
import time

HOST = "43.130.229.184"
USER = "root"
PW = "baifan100100"
REMOTE_BASE = "/root/soeasyhub_v2"

def debug_deploy():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password=PW)
    
    print("Uploading detail_new.html...")
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('detail_new.html', f'{REMOTE_BASE}/templates/tools/detail.html')
    
    print("Verifying remote file...")
    _, stdout, _ = ssh.exec_command(f'grep "The Experimenter\'s Paradise" {REMOTE_BASE}/templates/tools/detail.html')
    output = stdout.read().decode()
    if output:
        print("✅ Found string on remote file!")
    else:
        print("❌ String NOT found on remote file after upload!")
        # Let's see what IS there
        _, stdout, _ = ssh.exec_command(f'grep "expert-quote" {REMOTE_BASE}/templates/tools/detail.html | head -n 5')
        print("Remote expert-quotes found:")
        print(stdout.read().decode())
    
    print("Restarting service...")
    ssh.exec_command('pkill -9 -f gunicorn')
    time.sleep(2)
    ssh.exec_command(f'cd {REMOTE_BASE} && nohup python3 -m gunicorn -w 4 -b 127.0.0.1:9999 app:app --preload > gunicorn.log 2>&1 &')
    time.sleep(3)
    print("Deployment done.")
    ssh.close()

if __name__ == "__main__":
    debug_deploy()
