import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.130.229.184', username='root', password='baifan100100')
_, stdout, _ = ssh.exec_command('ls /etc/nginx/sites-enabled/')
print("Sites Enabled:", stdout.read().decode())
_, stdout, _ = ssh.exec_command('ls /etc/nginx/conf.d/')
print("Conf.d:", stdout.read().decode())
ssh.close()
