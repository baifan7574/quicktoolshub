import paramiko
from scp import SCPClient
import time

def deploy_fix():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    print("部署 Image Compressor 修复...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ 已连接到服务器")
        
        print("\n上传文件...")
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('templates/tools/detail.html', '/root/soeasyhub_v2/templates/tools/detail.html')
            print("  ✅ detail.html (修复了 API 调用逻辑)")
            
            scp.put('utils/image_tools.py', '/root/soeasyhub_v2/utils/image_tools.py')
            print("  ✅ image_tools.py (激进压缩算法)")
        
        print("\n重启服务...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(2)
        ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
        
        print("\n✅ 修复完成！")
        print("\n问题：")
        print("  ❌ Image Compressor 错误调用了 PDF 压缩 API")
        print("\n解决：")
        print("  ✅ 现在正确调用 /api/compress-image")
        print("  ✅ 使用激进的压缩算法（质量 60-75%）")
        print("\n请重新测试！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_fix()
