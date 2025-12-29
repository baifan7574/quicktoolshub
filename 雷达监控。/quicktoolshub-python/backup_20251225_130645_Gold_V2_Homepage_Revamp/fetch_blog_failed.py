"""
Download blog.py to debug why related articles logic failed
"""
import paramiko
from scp import SCPClient

def fetch_blog():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    with SCPClient(ssh.get_transport()) as scp:
        scp.get('/root/soeasyhub_v2/routes/blog.py', 'blog_failed_logic.py')
        
    ssh.close()
    print("Downloaded blog_failed_logic.py")

if __name__ == "__main__":
    fetch_blog()
