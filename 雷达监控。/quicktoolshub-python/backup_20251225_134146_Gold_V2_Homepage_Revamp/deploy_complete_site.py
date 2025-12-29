import paramiko
import os

def deploy_complete_templates():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    # 读取本地的完整模板文件
    with open('templates/base.html', 'r', encoding='utf-8') as f:
        base_html = f.read()
    
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()
    
    # 转义单引号以便在 shell 命令中使用
    base_html_escaped = base_html.replace("'", "'\"'\"'")
    index_html_escaped = index_html.replace("'", "'\"'\"'")
    
    commands = [
        # 创建目录结构
        "mkdir -p /root/soeasyhub_v2/templates/tools",
        "mkdir -p /root/soeasyhub_v2/templates/blog",
        
        # 上传 base.html
        f"cat > /root/soeasyhub_v2/templates/base.html << 'EOFBASE'\n{base_html}\nEOFBASE",
        
        # 上传 index.html
        f"cat > /root/soeasyhub_v2/templates/index.html << 'EOFINDEX'\n{index_html}\nEOFINDEX",
        
        # 重启服务
        "pkill -9 gunicorn || true",
        "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 -b 127.0.0.1:9999 app:app > debug.log 2>&1 &"
    ]
    
    for i, cmd in enumerate(commands):
        print(f"Step {i+1}/{len(commands)}: {cmd[:60]}...")
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
        stdout.channel.recv_exit_status()  # 等待命令完成
    
    ssh.close()
    print("\n✅ Complete templates deployed!")

if __name__ == "__main__":
    deploy_complete_templates()
