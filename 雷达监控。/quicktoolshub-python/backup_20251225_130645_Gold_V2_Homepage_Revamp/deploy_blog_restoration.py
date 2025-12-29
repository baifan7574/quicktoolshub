import paramiko
from scp import SCPClient

def deploy_blog():
    host = "43.130.229.184"
    user = "root"
    pw = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=pw)
    
    with SCPClient(ssh.get_transport()) as scp:
        print("Uploading blog_final.py as blog.py...")
        scp.put('blog_final.py', '/root/soeasyhub_v2/routes/blog.py')
        
    print("Restarting Gunicorn...")
    ssh.exec_command('pkill -HUP gunicorn || systemctl restart gunicorn')
    ssh.close()
    print("Blog restoration complete.")

if __name__ == "__main__":
    deploy_blog()
