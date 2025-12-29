import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.130.229.184', username='root', password='baifan100100')

print("Killing port 3000 processes...")
ssh.exec_command('pkill -9 -f "b 0.0.0.0:3000"')

import time
time.sleep(2)

_, stdout, _ = ssh.exec_command('ps aux | grep gunicorn | grep -v grep')
print("Remaining processes:")
print(stdout.read().decode())

ssh.close()
