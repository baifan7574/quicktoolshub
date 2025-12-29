
import paramiko

def final_detective():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    commands = {
        "1. Confirm My IP": "curl -s ifconfig.me",
        "2. Find THAT string": "grep -l -r 'Free Online Tools' /var /root /home /usr/share/nginx 2>/dev/null",
        "3. Check Other Web Servers": "ps aux | grep -E 'apache|httpd|openresty|caddy'",
        "4. Kill Nginx Entirely": "systemctl stop nginx && sleep 2 && netstat -tuln | grep :80"
    }
    
    for name, cmd in commands.items():
        print(f"--- {name} ---")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())
        print(stderr.read().decode())

    ssh.close()

if __name__ == "__main__":
    final_detective()
