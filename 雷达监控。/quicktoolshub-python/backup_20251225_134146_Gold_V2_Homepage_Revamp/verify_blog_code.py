"""
Verify blog.py content on server
"""
import paramiko

def verify_code():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    print("Checking for critical assignment line...")
    # grep for the assignment line
    cmd = "grep \"article\\['related_articles'\\] =\" /root/soeasyhub_v2/routes/blog.py"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    out = stdout.read().decode()
    if out.strip():
        print(f"✅ Found code: {out.strip()}")
    else:
        print("❌ Code NOT found!")
        
    ssh.close()

if __name__ == "__main__":
    verify_code()
