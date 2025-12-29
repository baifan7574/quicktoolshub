
import paramiko

def ghost_buster():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    # 这一段指令的目的是：
    # 1. 揪出那个正在作怪的旧文件夹并改名，让它无法再干扰
    # 2. 彻底重写 Nginx 逻辑
    commands = [
        # 寻找并改名所有可能的旧路径
        "mv /var/www/html /var/www/html_old_ghost || true",
        "mv /var/www/background_remover_tool /var/www/background_remover_old_ghost || true",
        
        # 强制重写 Nginx 核心配置 (这是最狠的一招)
        """cat > /etc/nginx/sites-available/soeasyhub_final.conf <<EOF
server {
    listen 80;
    server_name soeasyhub.com www.soeasyhub.com 43.130.229.184;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF""",
        "rm -f /etc/nginx/sites-enabled/*", # 删掉所有旧的软链接
        "ln -s /etc/nginx/sites-available/soeasyhub_final.conf /etc/nginx/sites-enabled/",
        
        # 重启 Nginx
        "systemctl restart nginx",
        
        # 重新确保后台程序在跑
        "pkill -9 -f gunicorn || true",
        "cd /var/www/soeasyhub_final && nohup gunicorn -w 4 -b 127.0.0.1:3000 app:app > gunicorn.log 2>&1 &"
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd[:50]}...")
        ssh.exec_command(cmd)

    ssh.close()
    print("Ghost busted! PLEASE refresh now.")

if __name__ == "__main__":
    ghost_buster()
