
import paramiko

def real_ultimate_fix():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    # 彻底的、物理层面的清除与接管
    commands = [
        # 1. 物理移除所有已知的旧代码路径
        "rm -rf /var/www/background_remover_tool",
        "rm -rf /root/quicktoolshub-python",
        "rm -rf /var/www/html",
        
        # 2. 彻底清理 Nginx 缓存
        "rm -rf /var/cache/nginx/*",
        "rm -rf /var/lib/nginx/proxy/*",
        
        # 3. 杀掉所有残留
        "pkill -9 python || true",
        "pkill -9 gunicorn || true",
        "pkill -9 pm2 || true", # 以防万一用了 pm2
        
        # 4. 在绝对全新的目录下部署
        "mkdir -p /root/SOEASY_V2_FINAL",
        "unzip -o /root/soeasyhub_new.zip -d /root/SOEASY_V2_FINAL",
        
        # 5. 暴力重写 Nginx (不留死角)
        """cat > /etc/nginx/sites-available/default <<EOF
server {
    listen 80 default_server;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:3005;
        proxy_set_header Host \$host;
    }
}
EOF""",
        "ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/",
        "systemctl restart nginx",
        
        # 6. 使用一个从未用过的端口 (3005)，彻底避开旧平衡
        "cd /root/SOEASY_V2_FINAL && nohup gunicorn -w 4 -b 127.0.0.1:3005 app:app > gunicorn.log 2>&1 &"
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd[:60]}...")
        ssh.exec_command(cmd)

    ssh.close()
    print("Physical clean up done. Visit IP now.")

if __name__ == "__main__":
    real_ultimate_fix()
