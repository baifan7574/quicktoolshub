import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.130.229.184', username='root', password='baifan100100')
_, stdout, _ = ssh.exec_command('grep -r "9999" /var/www/ /root/ 2>/dev/null | grep -v ".pyc" | head -n 20')
print(stdout.read().decode())
ssh.close()
