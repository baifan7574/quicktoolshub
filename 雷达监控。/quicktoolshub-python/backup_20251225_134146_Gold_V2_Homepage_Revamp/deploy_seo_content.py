import paramiko
from scp import SCPClient
import time

def deploy_seo_content():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    print("部署 Image Compressor 三件套 SEO 内容...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ 已连接到服务器")
        
        print("\n上传文件...")
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('templates/tools/detail.html', '/root/soeasyhub_v2/templates/tools/detail.html')
            print("  ✅ detail.html (添加了 Image Compressor 三件套)")
        
        print("\n重启服务...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(2)
        ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
        
        print("\n✅ 三件套已添加！")
        print("\nImage Compressor 现在包含：")
        print("  ✅ 工具功能")
        print("  ✅ Digital Presence 专业视角")
        print("  ✅ Mobile Performance Crisis")
        print("  ✅ SEO & Search Rankings")
        print("  ✅ Privacy & Security")
        print("  ✅ The Trust Signal")
        print("\n刷新页面查看完整内容！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_seo_content()
