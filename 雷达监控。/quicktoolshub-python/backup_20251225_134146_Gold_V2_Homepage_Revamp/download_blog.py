import paramiko
from scp import SCPClient

def download_blog():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    print("下载 blog.py...")
    with SCPClient(ssh.get_transport()) as scp:
        scp.get('/root/soeasyhub_v2/routes/blog.py', 'blog_check.py')
        
    ssh.close()

if __name__ == "__main__":
    download_blog()
