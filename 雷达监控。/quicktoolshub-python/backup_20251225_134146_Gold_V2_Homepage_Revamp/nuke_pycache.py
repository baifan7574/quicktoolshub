"""
Nuke __pycache__ and reinstall tools.py
"""
import paramiko
from scp import SCPClient
import time

def nuke_and_install():
    print("清理缓存并重新安装 tools.py...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    # 1. 停止服务
    print("停止服务...")
    ssh.exec_command("pkill -9 gunicorn")
    time.sleep(2)
    
    # 2. 清理 __pycache__ (关键一步!)
    print("清理 __pycache__...")
    ssh.exec_command("rm -rf /root/soeasyhub_v2/routes/__pycache__")
    ssh.exec_command("rm -rf /root/soeasyhub_v2/__pycache__")
    ssh.exec_command("find /root/soeasyhub_v2 -name '*.pyc' -delete")
    
    # 3. 替换 tools.py
    print("上传新文件...")
    with SCPClient(ssh.get_transport()) as scp:
        # 使用 tools_complete.py (硬编码完整版)
        scp.put('tools_complete.py', '/root/soeasyhub_v2/routes/tools.py')
        
    print("文件已替换")
    
    # 4. 启动服务
    print("启动服务...")
    cmd = "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ssh.exec_command(cmd)
    time.sleep(5)
    
    # 5. 验证
    stdin, stdout, stderr = ssh.exec_command("curl -I http://127.0.0.1:9999/tools/json-formatter")
    resp = stdout.read().decode()
    print("\n本地测试结果:")
    print(resp)
    
    ssh.close()

if __name__ == "__main__":
    nuke_and_install()
