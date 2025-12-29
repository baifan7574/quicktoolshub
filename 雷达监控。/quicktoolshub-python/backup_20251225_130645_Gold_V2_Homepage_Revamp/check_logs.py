import paramiko

def check_server_logs():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    commands = [
        "tail -200 /root/soeasyhub_v2/gunicorn.log"
    ]
    
    for cmd in commands:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read().decode()
        print(output)
            
    ssh.close()

if __name__ == "__main__":
    check_server_logs()
