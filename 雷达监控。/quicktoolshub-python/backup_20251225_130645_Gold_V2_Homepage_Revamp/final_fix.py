import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.130.229.184', username='root', password='baifan100100')

print("Checking PM2...")
_, stdout, _ = ssh.exec_command('pm2 list')
print(stdout.read().decode())

print("\nStopping PM2 managed process...")
ssh.exec_command('pm2 stop all')
ssh.exec_command('pm2 delete all')

import time
time.sleep(2)

print("\nKilling all remaining Gunicorn...")
ssh.exec_command('pkill -9 -f gunicorn')
time.sleep(2)

print("\nStarting correct Gunicorn on 9999...")
cmd = "cd /root/soeasyhub_v2 && nohup python3 -m gunicorn -w 4 -b 127.0.0.1:9999 app:app --preload > gunicorn.log 2>&1 &"
ssh.exec_command(cmd)
time.sleep(3)

_, stdout, _ = ssh.exec_command('ps aux | grep gunicorn | grep -v grep')
print("\nFinal status:")
print(stdout.read().decode())

_, stdout, _ = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" http://localhost:9999/tools/word-counter')
print(f"\nHTTP Status: {stdout.read().decode()}")

ssh.close()
print("\n✅ Complete fix applied!")
