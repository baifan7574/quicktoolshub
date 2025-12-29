"""
Cat app.py
"""
import paramiko

def cat_app():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    print("Reading app.py...")
    stdin, stdout, stderr = ssh.exec_command("cat /root/soeasyhub_v2/app.py")
    print(stdout.read().decode())
    
    ssh.close()

if __name__ == "__main__":
    cat_app()
