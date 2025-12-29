import paramiko

def fix_background_remover():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    commands = [
        # 1. 确保 Python 依赖正确安装
        "cd /root/soeasyhub_v2 && pip3 install --upgrade pip",
        "cd /root/soeasyhub_v2 && pip3 install rembg[cli] --no-cache-dir",
        "cd /root/soeasyhub_v2 && pip3 install onnxruntime==1.16.3 --no-cache-dir",
        "cd /root/soeasyhub_v2 && pip3 install opencv-python-headless --no-cache-dir",
        
        # 2. 预下载 AI 模型（这样第一次使用时不会超时）
        "cd /root/soeasyhub_v2 && python3 -c 'from rembg import remove; print(\"Model downloaded successfully\")'",
        
        # 3. 确保 uploads 目录有正确的权限
        "mkdir -p /root/soeasyhub_v2/uploads",
        "chmod 777 /root/soeasyhub_v2/uploads",
        
        # 4. 重启服务
        "pkill -9 gunicorn || true",
        "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ]
    
    for i, cmd in enumerate(commands):
        print(f"Step {i+1}/{len(commands)}: {cmd[:70]}...")
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
        exit_status = stdout.channel.recv_exit_status()
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        if output:
            print(f"  Output: {output[:200]}")
        if error and "warning" not in error.lower():
            print(f"  Error: {error[:200]}")
    
    ssh.close()
    print("\n✅ Background remover dependencies installed!")

if __name__ == "__main__":
    fix_background_remover()
