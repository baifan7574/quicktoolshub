import paramiko
from scp import SCPClient
import time

def deploy_image_converter():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    print("=" * 80)
    print("部署 Image Converter 功能")
    print("=" * 80)
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ 已连接到服务器")
        
        print("\n上传文件...")
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('utils/image_tools.py', '/root/soeasyhub_v2/utils/image_tools.py')
            print("  ✅ image_tools.py (添加了 convert_image 函数)")
            
            scp.put('routes/api.py', '/root/soeasyhub_v2/routes/api.py')
            print("  ✅ api.py (添加了 /api/convert-image 端点)")
            
            scp.put('templates/tools/detail.html', '/root/soeasyhub_v2/templates/tools/detail.html')
            print("  ✅ detail.html (添加了 Image Converter UI 和三件套)")
        
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
        print("✅ Image Converter 已部署！")
        print("=" * 80)
        
        print("\n🎉 新功能：")
        print("  ✅ convert_image() 函数 - 智能格式转换")
        print("  ✅ /api/convert-image 端点")
        print("  ✅ 支持格式: JPG, PNG, WebP")
        print("  ✅ 质量控制 (60-100%)")
        print("  ✅ 自动处理透明度")
        print("  ✅ 格式选择下拉菜单")
        print("  ✅ 质量滑块控制")
        
        print("\n📚 SEO 三件套：")
        print("  ✅ Format Compatibility 专业视角")
        print("  ✅ The Platform Trap")
        print("  ✅ Performance Factor")
        print("  ✅ SEO & Modern Web Standards")
        print("  ✅ Privacy & Security")
        print("  ✅ Quality Question")
        print("  ✅ Common Format Use Cases")
        
        print("\n🔧 功能特点：")
        print("  ✅ PNG → JPG (自动添加白色背景)")
        print("  ✅ JPG → PNG (保留质量)")
        print("  ✅ Any → WebP (现代网页格式)")
        print("  ✅ HEIC → JPG (iPhone 照片)")
        print("  ✅ 高质量 Lanczos 重采样")
        
        print("\n测试 URL:")
        print("  • http://soeasyhub.com/tools/image-converter")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_image_converter()
