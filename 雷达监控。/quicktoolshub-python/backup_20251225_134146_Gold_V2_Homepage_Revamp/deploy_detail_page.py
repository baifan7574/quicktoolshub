import paramiko

def deploy_tool_detail():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    # 读取本地的 detail.html
    with open('templates/tools/detail.html', 'r', encoding='utf-8') as f:
        detail_html = f.read()
    
    commands = [
        "mkdir -p /root/soeasyhub_v2/templates/tools",
        f"cat > /root/soeasyhub_v2/templates/tools/detail.html << 'EOFDETAIL'\n{detail_html}\nEOFDETAIL",
        "pkill -9 gunicorn || true",
        "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 120 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ]
    
    for i, cmd in enumerate(commands):
        print(f"Step {i+1}/{len(commands)}: {cmd[:70]}...")
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
        stdout.channel.recv_exit_status()
    
    ssh.close()
    print("\n✅ Tool detail page deployed!")

if __name__ == "__main__":
    deploy_tool_detail()
