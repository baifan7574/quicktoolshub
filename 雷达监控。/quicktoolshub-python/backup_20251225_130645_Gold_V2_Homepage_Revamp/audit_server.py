import paramiko

def check_server():
    host = "43.130.229.184"
    user = "root"
    pw = "baifan100100"
    remote_base = "/root/soeasyhub_v2"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=pw)
    
    commands = [
        f"ls -l {remote_base}/routes/tools.py",
        f"tail -n 5 {remote_base}/routes/tools.py",
        "ps aux | grep gunicorn",
        "netstat -tulpn | grep 3000",
        "netstat -tulpn | grep 9999",
        f"grep 'ARTICLES' {remote_base}/routes/blog.py | wc -l"
    ]
    
    for cmd in commands:
        print(f"--- Running: {cmd} ---")
        _, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())
        print(stderr.read().decode())
    
    ssh.close()

if __name__ == "__main__":
    check_server()
