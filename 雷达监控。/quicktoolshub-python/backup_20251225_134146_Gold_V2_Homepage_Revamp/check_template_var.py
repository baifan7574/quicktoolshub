"""
Download article.html to check template variable names
"""
import paramiko
from scp import SCPClient

def check_template():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    with SCPClient(ssh.get_transport()) as scp:
        scp.get('/root/soeasyhub_v2/templates/blog/article.html', 'article_debug.html')
        
    ssh.close()
    print("Downloaded article_debug.html")

if __name__ == "__main__":
    check_template()
