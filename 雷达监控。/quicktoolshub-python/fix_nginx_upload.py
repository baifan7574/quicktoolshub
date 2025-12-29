import paramiko

def fix_nginx_upload_limit():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    # 新的 Nginx 配置，增加上传限制到 50MB
    nginx_config = """server {
    listen 80 default_server;
    server_name _;
    
    # 增加上传文件大小限制到 50MB
    client_max_body_size 50M;
    
    location / {
        proxy_pass http://127.0.0.1:9999;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # 增加超时时间，因为 AI 处理需要时间
        proxy_read_timeout 300s;
        proxy_connect_timeout 300s;
    }
}"""
    
    commands = [
        f"echo '{nginx_config}' > /etc/nginx/sites-available/soeasyhub",
        "rm -f /etc/nginx/sites-enabled/*",
        "ln -s /etc/nginx/sites-available/soeasyhub /etc/nginx/sites-enabled/",
        "nginx -t",
        "systemctl restart nginx"
    ]
    
    for i, cmd in enumerate(commands):
        print(f"Step {i+1}/{len(commands)}: {cmd[:70]}...")
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
        exit_status = stdout.channel.recv_exit_status()
        
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        
        if output:
            print(f"  Output: {output}")
        if error:
            print(f"  Error: {error}")
    
    ssh.close()
    print("\n✅ Nginx upload limit increased to 50MB!")

if __name__ == "__main__":
    fix_nginx_upload_limit()
