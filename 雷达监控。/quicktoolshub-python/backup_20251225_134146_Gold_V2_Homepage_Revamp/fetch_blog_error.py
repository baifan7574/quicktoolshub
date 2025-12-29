"""
Fix blog.py syntax error manually
"""
import paramiko
from scp import SCPClient

def fetch_and_fix():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    print("Downloading blog.py...")
    with SCPClient(ssh.get_transport()) as scp:
        scp.get('/root/soeasyhub_v2/routes/blog.py', 'blog_syntax_error.py')
        
    ssh.close()
    
    # Read and find the error
    with open('blog_syntax_error.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    print(f"Total lines: {len(lines)}")
    
    # Check around line 1328
    start = max(0, 1320)
    end = min(len(lines), 1340)
    
    print(f"\nLines {start} to {end}:")
    for i in range(start, end):
        print(f"{i+1}: {lines[i].rstrip()}")

if __name__ == "__main__":
    fetch_and_fix()
