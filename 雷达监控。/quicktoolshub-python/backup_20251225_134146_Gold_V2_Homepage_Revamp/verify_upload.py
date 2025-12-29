"""
Cat tools.py content on server
"""
import paramiko

def cat_file():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    print("Checking tools.py content...")
    stdin, stdout, stderr = ssh.exec_command("cat /root/soeasyhub_v2/routes/tools.py")
    content = stdout.read().decode()
    
    if "json-formatter" in content:
        print("✅ Found 'json-formatter' in file content!")
        # Print the context lines
        for line in content.split('\n'):
            if "json-formatter" in line:
                print(f"  > {line.strip()}")
    else:
        print("❌ 'json-formatter' NOT found in file content!")
        
    ssh.close()

if __name__ == "__main__":
    cat_file()
