"""
Get Gunicorn logs to see DEBUG prints
"""
import paramiko

def get_logs():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    # 获取包含 DEBUG 的日志行，以及最后的错误
    cmd = "grep 'DEBUG' /root/soeasyhub_v2/gunicorn.log | tail -n 20"
    print("--- Debug Logs ---")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode())
    
    print("\n--- Last 20 Lines of Log ---")
    stdin, stdout, stderr = ssh.exec_command("tail -n 20 /root/soeasyhub_v2/gunicorn.log")
    print(stdout.read().decode())
    
    ssh.close()

if __name__ == "__main__":
    get_logs()
