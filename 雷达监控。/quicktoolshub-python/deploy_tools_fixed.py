import paramiko
from scp import SCPClient
import time

def deploy_tools_page_fixed():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    print("Connecting to server...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ Connected!")
        
        print("\nUploading files...")
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('routes/tools.py', '/root/soeasyhub_v2/routes/tools.py')
            print("  ✅ routes/tools.py uploaded")
        
        print("\nRestarting service...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(2)
        ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
        
        print("\n✅ Tools page updated successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_tools_page_fixed()
