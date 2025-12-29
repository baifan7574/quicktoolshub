import paramiko
from scp import SCPClient
import time

def deploy_pdf_merger():
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
            scp.put('templates/tools/pdf_merger.html', '/root/soeasyhub_v2/templates/tools/pdf_merger.html')
            print("  ✅ pdf_merger.html uploaded")
            
            scp.put('utils/pdf_tools.py', '/root/soeasyhub_v2/utils/pdf_tools.py')
            print("  ✅ pdf_tools.py uploaded")
            
            scp.put('routes/api.py', '/root/soeasyhub_v2/routes/api.py')
            print("  ✅ api.py uploaded")
            
            scp.put('routes/tools.py', '/root/soeasyhub_v2/routes/tools.py')
            print("  ✅ tools.py uploaded")
        
        print("\nRestarting service...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(2)
        ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
        
        print("\n✅ PDF Merger功能已完全升级！")
        print("\n新功能：")
        print("  ✅ 支持多文件上传")
        print("  ✅ 文件列表管理")
        print("  ✅ 专业 SEO 内容")
        print("  ✅ 高端设计风格")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_pdf_merger()
