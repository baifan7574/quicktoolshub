import paramiko
from scp import SCPClient
import time

def deploy_image_compressor():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    print("部署 Image Compressor 功能...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ 已连接到服务器")
        
        print("\n上传文件...")
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('utils/image_tools.py', '/root/soeasyhub_v2/utils/image_tools.py')
            print("  ✅ image_tools.py (添加了压缩功能)")
            
            scp.put('routes/api.py', '/root/soeasyhub_v2/routes/api.py')
            print("  ✅ api.py (添加了 compress-image API)")
        
        print("\n重启服务...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(2)
        ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
        
        print("\n✅ Image Compressor 后端已部署！")
        print("\n现在 Image Compressor 应该可以正常工作了")
        print("请测试：上传图片 → 压缩 → 下载")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_image_compressor()
