import paramiko

def fix_nginx_config():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    # 创建正确的 Nginx 配置
    config_content = """server {
    listen 80 default_server;
    server_name _;
    
    location / {
        proxy_pass http://127.0.0.1:9999;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}"""
    
    commands = [
        f"echo '{config_content}' > /etc/nginx/sites-available/soeasyhub",
        "rm -f /etc/nginx/sites-enabled/*",
        "ln -s /etc/nginx/sites-available/soeasyhub /etc/nginx/sites-enabled/",
        "nginx -t",
        "systemctl restart nginx"
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd[:60]}...")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if output:
            print(f"Output: {output}")
        if error:
            print(f"Error: {error}")
    
    ssh.close()
    print("\nNginx configuration fixed!")

if __name__ == "__main__":
    fix_nginx_config()
