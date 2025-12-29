
import paramiko

def deep_audit():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    commands = {
        "1. Real Source (CURL)": "curl -s http://localhost | grep -i 'title'",
        "2. Port 80 Owner": "lsof -i :80 || netstat -pan | grep ':80 '",
        "3. Find Old Files": "find /var/www /root -name 'index.html' -exec ls -lt {} + | head -n 10",
        "4. Check Docker": "docker ps",
        "5. Nginx Active Config": "nginx -T | grep 'server_name' -A 10"
    }
    
    for name, cmd in commands.items():
        print(f"--- {name} ---")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())
        print(stderr.read().decode())

    ssh.close()

if __name__ == "__main__":
    deep_audit()
