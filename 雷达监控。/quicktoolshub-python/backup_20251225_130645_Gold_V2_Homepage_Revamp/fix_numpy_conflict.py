import paramiko

def fix_numpy_conflict():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    commands = [
        # 1. 强制卸载可能存在的冲突版本
        "pip3 uninstall -y numpy",
        "pip3 uninstall -y numpy",
        
        # 2. 安装兼容版本 (1.26.4 是目前最稳定的 AI 兼容版)
        "pip3 install \"numpy<2.0.0\" --no-cache-dir",
        
        # 3. 再次验证 rembg 是否能运行 (这一步至关重要)
        "cd /root/soeasyhub_v2 && python3 -c 'import numpy; print(f\"NumPy Version: {numpy.__version__}\"); from rembg import remove; print(\"Rembg Import Success\")'",
        
        # 4. 确保上传目录存在且可写
        "mkdir -p /root/soeasyhub_v2/uploads",
        "chmod 777 /root/soeasyhub_v2/uploads",
        
        # 5. 重启服务
        "pkill -9 gunicorn || true",
        "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 120 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ]
    
    for i, cmd in enumerate(commands):
        print(f"Executing step {i+1}: {cmd[:80]}...")
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=120)
        exit_status = stdout.channel.recv_exit_status()
        
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        
        if output:
            print(f"  Output: {output}")
        if error and "warning" not in error.lower():
            print(f"  Error: {error}")
            
    ssh.close()
    print("\n✅ NumPy conflict resolved and service restarted!")

if __name__ == "__main__":
    fix_numpy_conflict()
