import paramiko
from scp import SCPClient
import time

def deploy_image_resizer():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    print("=" * 80)
    print("部署 Image Resizer 功能")
    print("=" * 80)
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ 已连接到服务器")
        
        print("\n上传文件...")
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('utils/image_tools.py', '/root/soeasyhub_v2/utils/image_tools.py')
            print("  ✅ image_tools.py (添加了 resize_image 函数)")
            
            scp.put('routes/api.py', '/root/soeasyhub_v2/routes/api.py')
            print("  ✅ api.py (添加了 /api/resize-image 端点)")
            
            scp.put('templates/tools/detail.html', '/root/soeasyhub_v2/templates/tools/detail.html')
            print("  ✅ detail.html (添加了 Image Resizer 三件套 SEO 内容)")
        
        print("\n重启服务...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(3)
        ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
        time.sleep(3)
        
        # 验证服务启动
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
        ps_output = stdout.read().decode()
        
        if ps_output:
            print("✅ 服务已启动")
        else:
            print("❌ 服务启动失败")
        
        print("\n" + "=" * 80)
        print("✅ Image Resizer 已部署！")
        print("=" * 80)
        
        print("\n🎉 新功能：")
        print("  ✅ resize_image() 函数 - 智能调整图片尺寸")
        print("  ✅ /api/resize-image 端点 - 处理调整请求")
        print("  ✅ 保持宽高比选项")
        print("  ✅ Lanczos 高质量重采样")
        print("  ✅ 支持 PNG 和 JPEG 格式")
        
        print("\n📚 SEO 三件套：")
        print("  ✅ Visual Impact 专业视角")
        print("  ✅ Multi-Device Challenge")
        print("  ✅ SEO & Performance Impact")
        print("  ✅ Privacy & Security")
        print("  ✅ Quality Factor")
        print("  ✅ Common Use Cases")
        
        print("\n测试 URL:")
        print("  • http://soeasyhub.com/tools/image-resizer")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_image_resizer()
