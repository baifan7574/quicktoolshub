"""
Check Gunicorn CWD
"""
import paramiko

def check_cwd():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    print("Checking Gunicorn processes...")
    stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
    print(stdout.read().decode())
    
    print("\nChecking process CWDs...")
    # Find all gunicorn pids and ls -l /proc/PID/cwd
    stdin, stdout, stderr = ssh.exec_command("pgrep gunicorn")
    pids = stdout.read().decode().strip().split('\n')
    
    for pid in pids:
         if pid:
             stdin, stdout, stderr = ssh.exec_command(f"ls -l /proc/{pid}/cwd")
             print(f"PID {pid}: {stdout.read().decode().strip()}")
             
    ssh.close()

if __name__ == "__main__":
    check_cwd()
