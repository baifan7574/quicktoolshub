"""
Deploy tool update to production server
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
        
        print("Uploading routes/blog.py...")
        scp.put('blog_new.py', f'{remote_base}/routes/blog.py')
        
        print("Uploading templates/tools/detail.html...")
        scp.put('detail_new.html', f'{remote_base}/templates/tools/detail.html')
        
    print("Restarting Gunicorn...")
    # 尝试多种重启方式以确保生效
    ssh.exec_command(f'cd {remote_base} && pkill -HUP gunicorn || systemctl restart gunicorn || supervisorctl restart soeasyhub')
    
    print("Deployment complete.")
    ssh.close()

if __name__ == "__main__":
    deploy()
