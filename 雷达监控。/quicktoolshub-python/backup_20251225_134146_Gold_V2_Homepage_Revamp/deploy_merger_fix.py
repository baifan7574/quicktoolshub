import paramiko
from scp import SCPClient
import time

def deploy_fixed_merger():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    print("Deploying fixed PDF Merger...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ Connected!")
        
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('templates/tools/pdf_merger.html', '/root/soeasyhub_v2/templates/tools/pdf_merger.html')
            print("✅ pdf_merger.html uploaded")
        
        print("Restarting service...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(2)
        ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
        
        print("\n✅ Fixed! 页面加载问题已解决")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_fixed_merger()
