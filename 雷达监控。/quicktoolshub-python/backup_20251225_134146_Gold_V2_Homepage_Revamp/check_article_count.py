"""
Check article count on server
"""
import paramiko

def check_count():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    cmd = 'python3 -c "from routes.blog import ARTICLES; print(f\'TOTAL ARTICLES: {len(ARTICLES)}\'); print([a[\'slug\'] for a in ARTICLES])"'
    
    print("Checking article count...")
    stdin, stdout, stderr = ssh.exec_command(f"cd /root/soeasyhub_v2 && {cmd}")
    
    out = stdout.read().decode()
    err = stderr.read().decode()
    
    print("STDOUT:", out)
    if err:
        print("STDERR:", err)
        
    ssh.close()

if __name__ == "__main__":
    check_count()
