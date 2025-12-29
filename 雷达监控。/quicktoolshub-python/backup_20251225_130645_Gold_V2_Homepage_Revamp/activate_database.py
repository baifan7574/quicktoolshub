
import paramiko

def activate_database():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    # 注入真实的数据库地址和密钥
    commands = [
        # 1. 创建全新的 .env 文件
        """cat > /root/SOEASY_V2_FINAL/.env <<EOF
SUPABASE_URL=https://nbfzhxgkfljeuoncujum.supabase.co
SUPABASE_KEY=sb_publishable_fXPwQ3q1K-shVTvskWv0Xw_vsQrhBoK
SECRET_KEY=so-easy-hub-secret-2025
FLASK_DEBUG=False
EOF""",
        
        # 2. 确保同步一份到您要求的备份目录
        "cp /root/SOEASY_V2_FINAL/.env /root/quicktoolshub-python/.env",
        
        # 3. 杀掉旧进程并重新启动服务
        "pkill -9 gunicorn || true",
        "cd /root/SOEASY_V2_FINAL && nohup gunicorn -w 4 -b 127.0.0.1:9999 app:app --preload > gunicorn.log 2>&1 &"
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd[:60]}...")
        ssh.exec_command(cmd)

    ssh.close()
    print("Database Heartbeat Activated!")

if __name__ == "__main__":
    activate_database()
