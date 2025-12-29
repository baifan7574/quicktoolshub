import paramiko
from scp import SCPClient

def install_ghostscript_and_deploy():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    commands = [
        # 1. 安装 Ghostscript
        "apt-get update",
        "apt-get install -y ghostscript",
        
        # 2. 验证安装
        "gs --version",
    ]
    
    for i, cmd in enumerate(commands):
        print(f"Step {i+1}/{len(commands)}: {cmd[:70]}...")
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
        exit_status = stdout.channel.recv_exit_status()
        
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        
        if output:
            print(f"  Output: {output[:200]}")
        if error and "warning" not in error.lower():
            print(f"  Error: {error[:200]}")
    
    # 3. 上传新的 PDF 工具代码
    print("\nUploading updated PDF tools...")
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('utils/pdf_tools.py', '/root/soeasyhub_v2/utils/pdf_tools.py')
    
    # 4. 重启服务
    print("Restarting service...")
    ssh.exec_command("pkill -9 gunicorn || true")
    ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 120 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
    
    ssh.close()
    print("\n✅ Ghostscript installed and PDF tools updated!")

if __name__ == "__main__":
    install_ghostscript_and_deploy()
