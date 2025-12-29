"""
Final Deploy: Remove debug mode, upload robust template
"""
import paramiko
from scp import SCPClient
import time

def final_deploy():
    print("Preparing final blog.py (no debug)...")
    with open('blog_assignment_fix.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
    # blog_assignment_fix.py already has the correct logic without debug mode!
    # Reuse it.
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    with SCPClient(ssh.get_transport()) as scp:
        print("Uploading blog.py...")
        scp.put('blog_assignment_fix.py', '/root/soeasyhub_v2/routes/blog.py')
        
        print("Uploading article.html template...")
        scp.put('article_robust.html', '/root/soeasyhub_v2/templates/blog/article.html')
        
    print("Restarting...")
    ssh.exec_command("pkill -9 gunicorn || true")
    time.sleep(2)
    cmd = "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ssh.exec_command(cmd)
    
    time.sleep(5)
    print("All fixed!")
    ssh.close()

if __name__ == "__main__":
    final_deploy()
