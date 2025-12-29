import paramiko
from scp import SCPClient

def deploy_full_site():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    print("Uploading complete codebase...")
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('full_deploy.zip', '/root/full_deploy.zip')
    
    print("Extracting and setting up...")
    commands = [
        "rm -rf /root/soeasyhub_v2",
        "mkdir -p /root/soeasyhub_v2",
        "cd /root && unzip -o full_deploy.zip -d soeasyhub_v2",
        
        # 创建 .env 文件
        """cat > /root/soeasyhub_v2/.env <<EOF
SUPABASE_URL=https://nbfzhxgkfljeuoncujum.supabase.co
SUPABASE_KEY=sb_publishable_fXPwQ3q1K-shVTvskWv0Xw_vsQrhBoK
SECRET_KEY=so-easy-hub-secret-2025
FLASK_DEBUG=False
EOF""",
        
        # 创建 uploads 目录
        "mkdir -p /root/soeasyhub_v2/uploads",
        
        # 重启服务
        "pkill -9 gunicorn || true",
        "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 120 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd[:60]}...")
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=60)
        stdout.channel.recv_exit_status()
    
    ssh.close()
    print("\n✅ Full site deployed!")

if __name__ == "__main__":
    deploy_full_site()
