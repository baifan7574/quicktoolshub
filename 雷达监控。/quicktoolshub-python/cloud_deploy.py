
import paramiko
from scp import SCPClient
import os

def deploy():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    print(f"Connecting to {hostname}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    # 1. 上传文件
    print("Uploading code package...")
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('deploy.zip', '/root/soeasyhub_new.zip')
    
    # 2. 远程执行部署
    print("Executing remote deployment commands...")
    commands = [
        "mkdir -p /root/soeasyhub_v2",
        "unzip -o /root/soeasyhub_new.zip -d /root/soeasyhub_v2",
        "cd /root/soeasyhub_v2 && pip3 install --upgrade pip",
        "cd /root/soeasyhub_v2 && pip3 install -r requirements.txt",
        # 使用 gunicorn 后台运行
        "pkill gunicorn || true",
        "nohup gunicorn -w 4 -b 0.0.0.0:3000 app:app > gunicorn.log 2>&1 &"
    ]
    
    for cmd in commands:
        print(f"Running: {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        # 打印输出以便调试
        out = stdout.read().decode()
        err = stderr.read().decode()
        if out: print(out)
        if err: print(err)

    ssh.close()
    print("Deployment Complete! Visit http://43.130.229.184:3000")

if __name__ == "__main__":
    deploy()
