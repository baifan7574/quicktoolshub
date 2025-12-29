
import paramiko

def fetch_logs():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 使用你之前的凭证
        ssh.connect('43.130.229.184', username='root', password='baifan100100')
        
        # 尝试读取 gunicorn 的输出
        # 我们假设 gunicorn 是在前台运行或者有日志文件
        # 先查看最近运行的 python 进程
        print("--- Process List ---")
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn")
        print(stdout.read().decode())

        # 尝试查找日志文件。通常在 /root/soeasyhub_v2/ 下可能有 gunicorn.log 或者 nohup.out
        print("--- Log File Check ---")
        stdin, stdout, stderr = ssh.exec_command("ls -F /root/soeasyhub_v2/")
        print(stdout.read().decode())
        
        # 读取可能的日志文件最后 50 行
        print("--- Gunicorn Log Tail ---")
        # 假设 deploy_stable.py 使用了 nohup 或者将输出重定向到了某个文件
        # 如果没有，我们可能只能看到 nginx 的 error.log
        stdin, stdout, stderr = ssh.exec_command("tail -n 50 /root/soeasyhub_v2/gunicorn.log")
        print(stdout.read().decode())
        
        # 同时也看看 Nginx 的错误日志，以防万一
        print("--- Nginx Error Log ---")
        stdin, stdout, stderr = ssh.exec_command("tail -n 20 /var/log/nginx/error.log")
        print(stdout.read().decode())

        ssh.close()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    fetch_logs()
