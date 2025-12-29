import paramiko

def fix_timeout_issues():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    # 新的 Nginx 配置，增加超时到 10 分钟
    nginx_config = """server {
    listen 80 default_server;
    server_name _;
    
    client_max_body_size 50M;
    
    location / {
        proxy_pass http://127.0.0.1:9999;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # 增加超时时间到 10 分钟
        proxy_read_timeout 600s;
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
    }
}"""
    
    commands = [
        # 1. 更新 Nginx 配置
        f"echo '{nginx_config}' > /etc/nginx/sites-available/soeasyhub",
        "nginx -t",
        "systemctl reload nginx",
        
        # 2. 重启 Gunicorn，增加超时到 5 分钟
        "pkill -9 gunicorn || true",
        "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &",
        
        # 3. 等待服务启动
        "sleep 3",
        "ps aux | grep gunicorn | grep -v grep",
    ]
    
    for i, cmd in enumerate(commands):
        print(f"Step {i+1}/{len(commands)}: {cmd[:70]}...")
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
        stdout.channel.recv_exit_status()
        
        output = stdout.read().decode().strip()
        if output:
            print(f"  {output[:200]}")
    
    ssh.close()
    print("\n✅ Timeout settings increased to 5-10 minutes!")

if __name__ == "__main__":
    fix_timeout_issues()
