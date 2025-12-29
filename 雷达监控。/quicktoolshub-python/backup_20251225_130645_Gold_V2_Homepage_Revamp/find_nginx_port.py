import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.130.229.184', username='root', password='baifan100100')
_, stdout, _ = ssh.exec_command('grep -r "proxy_pass" /etc/nginx/sites-enabled/')
print(stdout.read().decode())
ssh.close()
