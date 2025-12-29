"""
紧急排查：查看 Gunicorn 最新错误日志
"""
import paramiko
import time

def check_logs():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    print("正在获取服务器日志...")
    # 获取最后 100 行日志
    stdin, stdout, stderr = ssh.exec_command("tail -n 100 /root/soeasyhub_v2/gunicorn.log")
    logs = stdout.read().decode()
    print("="*50)
    print(logs)
    print("="*50)
    
    ssh.close()

if __name__ == "__main__":
    check_logs()
