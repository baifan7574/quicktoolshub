"""
Check if article exists in blog.py
"""
import paramiko

def check_article():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    print("Checking blog.py for json article...")
    # 只需查有没有这个 slug 字符串
    stdin, stdout, stderr = ssh.exec_command("grep 'json-formatter-online-free-guide' /root/soeasyhub_v2/routes/blog.py")
    result = stdout.read().decode()
    
    if result:
        print("✅ Found article slug in file!")
        print(result.strip())
    else:
        print("❌ Article slug NOT found anywhere in file!")
        
    ssh.close()

if __name__ == "__main__":
    check_article()
