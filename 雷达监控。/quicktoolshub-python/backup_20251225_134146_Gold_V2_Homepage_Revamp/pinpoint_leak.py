
import paramiko

def pinpoint_leak():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    # 强制查看 Nginx 进程正在打开的文件
    commands = {
        "Active Nginx Working Dir": "ls -l /proc/$(pgrep -n nginx)/cwd",
        "Nginx Master Config Raw": "cat /etc/nginx/nginx.conf",
        "Dump All Configs": "nginx -T",
        "Kill & Show": "systemctl stop nginx && netstat -tuln | grep :80"
    }
    
    for name, cmd in commands.items():
        print(f"--- {name} ---")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())
    
    ssh.close()

if __name__ == "__main__":
    pinpoint_leak()
