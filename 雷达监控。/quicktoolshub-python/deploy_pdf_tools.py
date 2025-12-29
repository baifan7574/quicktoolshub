import paramiko
from scp import SCPClient

def deploy_pdf_tools():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    print("Uploading updated PDF tools...")
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('utils/pdf_tools.py', '/root/soeasyhub_v2/utils/pdf_tools.py')
    
    commands = [
        "pkill -9 gunicorn || true",
        "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 120 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd[:70]}...")
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
        stdout.channel.recv_exit_status()
    
    ssh.close()
    print("\n✅ PDF tools updated and service restarted!")

if __name__ == "__main__":
    deploy_pdf_tools()
