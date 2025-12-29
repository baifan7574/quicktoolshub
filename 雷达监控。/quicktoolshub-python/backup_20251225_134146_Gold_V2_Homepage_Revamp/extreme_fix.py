
import paramiko

def extreme_fix():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    commands = [
        # 1. 彻底杀掉所有可能的 Python 后台
        "pkill -9 -f gunicorn || true",
        "pkill -9 -f python || true",
        
        # 2. 强力重写 Nginx 配置文件 (彻底摒弃之前的逻辑)
        # 我们创建一个极简且正确的配置
        """cat > /etc/nginx/sites-available/soeasyhub_final.conf <<EOF
server {
    listen 80;
    server_name soeasyhub.com www.soeasyhub.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }

    location /static {
        alias /var/www/soeasyhub_final/static;
    }
}
EOF""",
        # 联系到启用目录
        "ln -sf /etc/nginx/sites-available/soeasyhub_final.conf /etc/nginx/sites-enabled/soeasyhub.com",
        "rm -f /etc/nginx/sites-enabled/background_remover_tool", # 删掉可能的干扰项
        
        # 3. 重启 Nginx
        "nginx -t && systemctl restart nginx",
        
        # 4. 在新目录下启动
        "cd /var/www/soeasyhub_final && nohup gunicorn -w 4 -b 127.0.0.1:3000 app:app > gunicorn.log 2>&1 &"
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd[:50]}...")
        ssh.exec_command(cmd)

    ssh.close()
    print("Extreme fix done. Please refresh your browser now.")

if __name__ == "__main__":
    extreme_fix()
