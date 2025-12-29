"""
部署完整的 tools.py
"""
import paramiko
from scp import SCPClient
import time

def deploy_complete():
    print("正在部署完整的 tools.py ...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('tools_complete.py', '/root/soeasyhub_v2/routes/tools.py')
        print("✅ tools.py 已上传")
    
    print("🔄 重启服务...")
    # 强制杀死所有 gunicorn 进程
    ssh.exec_command("pkill -9 gunicorn || true")
    time.sleep(3)
    
    # 启动
    cmd = "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ssh.exec_command(cmd)
    time.sleep(5)
    
    # 检查
    stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
    result = stdout.read().decode()
    if result:
        print("✅ 服务启动成功！")
        print(result)
        print("\n最终确认：请访问 http://soeasyhub.com/tools/json-formatter")
    else:
        print("❌ 服务未启动，查看日志...")
        stdin, stdout, stderr = ssh.exec_command("tail -n 20 /root/soeasyhub_v2/gunicorn.log")
        print(stdout.read().decode())
    
    ssh.close()

if __name__ == "__main__":
    deploy_complete()
