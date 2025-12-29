import paramiko
from scp import SCPClient

def deploy_tools_page():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    print("Uploading updated files...")
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('templates/tools/index.html', '/root/soeasyhub_v2/templates/tools/index.html')
        scp.put('routes/tools.py', '/root/soeasyhub_v2/routes/tools.py')
    
    commands = [
        "pkill -9 gunicorn || true",
        "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd[:70]}...")
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
        stdout.channel.recv_exit_status()
    
    ssh.close()
    print("\n✅ Tools page updated with premium design and category counts!")

if __name__ == "__main__":
    deploy_tools_page()
