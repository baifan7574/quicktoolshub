import paramiko

def test_ghostscript_on_server():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    commands = [
        # 测试 Ghostscript 是否可用
        "which gs",
        "gs --version",
        
        # 检查 Python 是否能调用 Ghostscript
        "cd /root/soeasyhub_v2 && python3 -c 'import subprocess; result = subprocess.run([\"gs\", \"--version\"], capture_output=True, text=True); print(result.stdout)'",
        
        # 查看最近的应用日志
        "tail -50 /root/soeasyhub_v2/gunicorn.log | grep -i 'ghost\\|compress\\|pdf' || echo 'No compression logs found'",
    ]
    
    for cmd in commands:
        print(f"\n{'='*80}")
        print(f"Command: {cmd}")
        print('='*80)
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
        
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        
        if output:
            print(f"Output:\n{output}")
        if error:
            print(f"Error:\n{error}")
    
    ssh.close()

if __name__ == "__main__":
    test_ghostscript_on_server()
