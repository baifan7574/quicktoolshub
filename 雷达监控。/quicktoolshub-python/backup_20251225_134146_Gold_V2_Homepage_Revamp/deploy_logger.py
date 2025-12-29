"""
Deploy Debug Logger
"""
import paramiko
from scp import SCPClient
import time

def deploy_logger():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    print("停止服务...")
    ssh.exec_command("pkill -9 gunicorn")
    ssh.exec_command("rm -f /root/soeasyhub_v2/debug.txt") # 清除旧日志
    
    print("上传...")
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('tools_debug_log.py', '/root/soeasyhub_v2/routes/tools.py')
        
    print("启动...")
    cmd = "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ssh.exec_command(cmd)
    time.sleep(5)
    
    # 触发请求
    print("发送请求...")
    ssh.exec_command("curl -I http://127.0.0.1:9999/tools/json-formatter")
    
    # 读取日志
    print("\nDebug 日志内容:")
    stdin, stdout, stderr = ssh.exec_command("cat /root/soeasyhub_v2/debug.txt")
    print(stdout.read().decode())
    
    ssh.close()

if __name__ == "__main__":
    deploy_logger()
