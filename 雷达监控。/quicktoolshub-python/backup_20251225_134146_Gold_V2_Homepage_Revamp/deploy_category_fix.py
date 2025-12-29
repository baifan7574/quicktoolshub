"""
Deploy Category Count Fix to production server
"""
import paramiko
from scp import SCPClient
import os

def deploy():
    # Server Details
    host = "43.130.229.184"
    user = "root"
    pw = "baifan100100"
    remote_base = "/root/soeasyhub_v2"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=pw, timeout=60)
    
    with SCPClient(ssh.get_transport()) as scp:
        print("Uploading routes/tools.py...")
        scp.put('tools_new.py', f'{remote_base}/routes/tools.py')
        
        print("Uploading templates/tools/index.html...")
        scp.put('tools_index_new.html', f'{remote_base}/templates/tools/index.html')
        
    print("Restarting Gunicorn...")
    ssh.exec_command(f'cd {remote_base} && pkill -HUP gunicorn || systemctl restart gunicorn')
    
    print("Deployment complete.")
    ssh.close()

if __name__ == "__main__":
    deploy()
