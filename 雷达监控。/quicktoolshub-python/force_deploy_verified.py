import paramiko
import os

HOST = "43.130.229.184"
USER = "root"
PW = "baifan100100"
REMOTE_BASE = "/root/soeasyhub_v2"

FILES_TO_DEPLOY = {
    'tools_new.py': f'{REMOTE_BASE}/routes/tools.py',
    'blog_final.py': f'{REMOTE_BASE}/routes/blog.py',
    'detail_new.html': f'{REMOTE_BASE}/templates/tools/detail.html',
    'app.py': f'{REMOTE_BASE}/app.py',
    'templates/index.html': f'{REMOTE_BASE}/templates/index.html',
    'templates/pages/search.html': f'{REMOTE_BASE}/templates/pages/search.html',
    'static/img/michael_avatar.png': f'{REMOTE_BASE}/static/img/michael_avatar.png'
}

def force_deploy():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password=PW)
    sftp = ssh.open_sftp()
    
    for local, remote in FILES_TO_DEPLOY.items():
        print(f"Uploading {local} to {remote}...")
        if not os.path.exists(local):
            print(f"Local file {local} not found!")
            continue
            
        # Ensure remote directory exists
        remote_dir = os.path.dirname(remote)
        try:
            ssh.exec_command(f'mkdir -p {remote_dir}')
        except:
            pass
        
        # Remove remote file if exists to bypass any write locks
        try:
            sftp.remove(remote)
        except:
            pass
            
        sftp.put(local, remote)
        
        # Verify
        stat = sftp.stat(remote)
        local_size = os.path.getsize(local)
        if stat.st_size == local_size:
            print(f"Verified {local} -> {remote} ({local_size} bytes)")
        else:
            print(f"Mismatch! Local: {local_size}, Remote: {stat.st_size}")

    print("Restarting Gunicorn...")
    ssh.exec_command('pkill -9 -f gunicorn')
    cmd = f"cd {REMOTE_BASE} && nohup python3 -m gunicorn -w 4 -b 127.0.0.1:9999 app:app --preload > gunicorn_force.log 2>&1 &"
    ssh.exec_command(cmd)
    ssh.close()
    print("Done.")

if __name__ == "__main__":
    force_deploy()
