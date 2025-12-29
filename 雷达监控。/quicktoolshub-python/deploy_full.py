"""
Full deploy script for URL Encoder and SEO fix
"""
import paramiko
from scp import SCPClient
import os

def deploy():
    # Server Details
    host = "43.130.229.184"
    user = "root"
    pw = "baifan100100"
    remote_base = "/root/soeasyhub_v2"
    
    # Local check before upload
    print("Verifying local syntax...")
    import subprocess
    result = subprocess.run(['python', '-m', 'py_compile', 'tools_new.py', 'blog_final.py'], capture_output=True)
    if result.returncode != 0:
        print("Syntax error detected locally. Aborting.")
        print(result.stderr.decode())
        return

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=pw, timeout=60)
    
    with SCPClient(ssh.get_transport()) as scp:
        print("Uploading routes/tools.py...")
        scp.put('tools_new.py', f'{remote_base}/routes/tools.py')
        
        print("Uploading routes/blog.py...")
        # CRITICAL: Use blog_final.py which contains ALL articles
        scp.put('blog_final.py', f'{remote_base}/routes/blog.py')
        
        print("Uploading templates/tools/detail.html...")
        scp.put('detail_new.html', f'{remote_base}/templates/tools/detail.html')
        
        print("Uploading templates/tools/index.html...")
        # Check if file exists, if not use a fallback or warn
        if os.path.exists('tools_index_new.html'):
            scp.put('tools_index_new.html', f'{remote_base}/templates/tools/index.html')
        
    print("Restarting Gunicorn (HARD RESTART)...")
    # pkill -f to find the full command line, then sleeping and restarting
    # Using port 9999 as per project standards/Nginx configuration
    restart_cmd = f"cd {remote_base} && pkill -f gunicorn; sleep 2; nohup python3 -m gunicorn -w 4 -b 127.0.0.1:9999 app:app --preload > gunicorn.log 2>&1 &"
    
    # We use exec_command but need to ensure it doesn't wait forever if & is used
    ssh.exec_command(restart_cmd)
    
    print("Deployment complete. Waiting 5s for startup...")
    import time
    time.sleep(5)
    
    # Check if process is back
    _, stdout, _ = ssh.exec_command("ps aux | grep gunicorn")
    print(stdout.read().decode())
    
    ssh.close()

if __name__ == "__main__":
    deploy()
