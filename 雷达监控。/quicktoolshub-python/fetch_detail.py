"""
Download detail.html for inspection
"""
import paramiko
from scp import SCPClient

def fetch_html():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    with SCPClient(ssh.get_transport()) as scp:
        scp.get('/root/soeasyhub_v2/templates/tools/detail.html', 'detail_messy.html')
        
    ssh.close()
    print("Downloaded detail_messy.html")

if __name__ == "__main__":
    fetch_html()
