import paramiko

def deploy_css():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    # 读取本地 CSS 文件
    with open('static/css/premium.css', 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # 转义单引号
    css_escaped = css_content.replace("'", "'\"'\"'")
    
    commands = [
        "mkdir -p /root/soeasyhub_v2/static/css",
        "mkdir -p /root/soeasyhub_v2/static/js",
        f"cat > /root/soeasyhub_v2/static/css/premium.css << 'EOFCSS'\n{css_content}\nEOFCSS",
        # 创建一个简单的 main.js
        "echo '// SoEasyHub main.js' > /root/soeasyhub_v2/static/js/main.js",
        # 重启服务
        "pkill -9 gunicorn || true",
        "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ]
    
    for i, cmd in enumerate(commands):
        print(f"Step {i+1}/{len(commands)}: {cmd[:60]}...")
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
        stdout.channel.recv_exit_status()
    
    ssh.close()
    print("\n✅ CSS and static files deployed!")

if __name__ == "__main__":
    deploy_css()
