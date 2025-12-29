"""
Deploy Fixed Detail HTML
"""
import paramiko
from scp import SCPClient
import time

def deploy_detail():
    print("Uploading fixed detail.html...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('detail_clean_fixed.html', '/root/soeasyhub_v2/templates/tools/detail.html')
        
    print("Restarting Gunicorn...")
    ssh.exec_command("pkill -9 gunicorn || true")
    time.sleep(2)
    cmd = "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ssh.exec_command(cmd)
    time.sleep(5)
    
    print("Checking status...")
    stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
    print(stdout.read().decode())
    
    ssh.close()

if __name__ == "__main__":
    deploy_detail()
