import paramiko
from scp import SCPClient

host = "43.130.229.184"
user = "root"
pw = "baifan100100"
remote_base = "/root/soeasyhub_v2"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=pw)

with SCPClient(ssh.get_transport()) as scp:
    print("Downloading current homepage...")
    scp.get(f'{remote_base}/templates/index.html', 'index_current.html')
    print("Downloaded to index_current.html")

ssh.close()
