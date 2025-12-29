import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.130.229.184', username='root', password='baifan100100')
_, stdout, _ = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/tools/word-counter')
print(f'HTTP Status: {stdout.read().decode()}')
ssh.close()
