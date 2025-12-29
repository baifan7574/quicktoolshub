
import paramiko

def fix_502_and_sync_env():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    commands = [
        # 1. 在正确的位置同步 .env (使用您刚才给我的新钥匙)
        """cat > /root/soeasyhub_v2/.env <<EOF
SUPABASE_URL=https://nbfzhxgkfljeuoncujum.supabase.co
SUPABASE_KEY=sb_publishable_fXPwQ3q1K-shVTvskWv0Xw_vsQrhBoK
SECRET_KEY=so-easy-hub-secret-2025
FLASK_DEBUG=False
EOF""",
        
        # 2. 杀掉所有旧版
        "pkill -9 gunicorn || true",
        "pkill -9 python || true",
        
        # 3. 强制在 9999 端口启动 (匹配 Nginx 配置)
        "cd /root/soeasyhub_v2 && nohup gunicorn -w 4 -b 127.0.0.1:9999 app:app --preload > gunicorn.log 2>&1 &",
        
        # 4. 检查 Nginx 确保它指向 9999
        "sed -i 's/127.0.0.1:[0-9]*/127.0.0.1:9999/g' /etc/nginx/sites-enabled/*",
        "systemctl restart nginx"
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd[:60]}...")
        ssh.exec_command(cmd)

    ssh.close()
    print("Port fixed and Env synced. Please try soeasyhub.com again.")

if __name__ == "__main__":
    fix_502_and_sync_env()
