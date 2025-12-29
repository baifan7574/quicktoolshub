
import paramiko

def final_victory():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    commands = [
        # 彻底物理抹除
        "rm -rf /var/www/background_remover_tool",
        "rm -rf /var/www/html",
        "rm -rf /root/quicktoolshub-python",
        
        # 清空所有的 Nginx 干扰项
        "rm -f /etc/nginx/sites-enabled/*",
        
        # 创建一个绝对正确的 Nginx 配置文件
        """cat > /etc/nginx/sites-available/FINAL_SOEASY <<EOF
server {
    listen 80 default_server;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:9999;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF""",
        "ln -sf /etc/nginx/sites-available/FINAL_SOEASY /etc/nginx/sites-enabled/",
        "pkill -9 python || true",
        "pkill -9 gunicorn || true",
        "systemctl restart nginx",
        
        # 在 9999 端口启动最新的代码
        "cd /root/SOEASY_V2_FINAL && nohup gunicorn -w 4 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ]
    
    for cmd in commands:
        print(f"Running: {cmd[:50]}...")
        ssh.exec_command(cmd)

    ssh.close()

if __name__ == "__main__":
    final_victory()
