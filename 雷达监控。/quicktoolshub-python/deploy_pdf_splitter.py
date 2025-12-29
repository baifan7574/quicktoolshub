import paramiko
from scp import SCPClient
import time

def deploy_pdf_splitter():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    print("Deploying PDF Splitter...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ Connected!")
        
        print("\nUploading files...")
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('templates/tools/pdf_splitter.html', '/root/soeasyhub_v2/templates/tools/pdf_splitter.html')
            print("  ✅ pdf_splitter.html")
            
            scp.put('utils/pdf_tools.py', '/root/soeasyhub_v2/utils/pdf_tools.py')
            print("  ✅ pdf_tools.py")
            
            scp.put('routes/api.py', '/root/soeasyhub_v2/routes/api.py')
            print("  ✅ api.py")
            
            scp.put('routes/tools.py', '/root/soeasyhub_v2/routes/tools.py')
            print("  ✅ tools.py")
        
        print("\nRestarting service...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(2)
        ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
        
        print("\n✅ PDF Splitter 已部署！")
        print("\n新功能：")
        print("  ✅ 按范围分割 (例如: 1-5, 10-15)")
        print("  ✅ 提取特定页面 (例如: 1, 3, 5, 7)")
        print("  ✅ 专业 SEO 内容")
        print("  ✅ 高端设计风格")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_pdf_splitter()
