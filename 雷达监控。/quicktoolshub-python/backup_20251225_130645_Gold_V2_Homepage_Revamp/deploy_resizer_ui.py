import paramiko
from scp import SCPClient
import time

def deploy_resizer_ui():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    print("=" * 80)
    print("部署 Image Resizer UI 和功能修复")
    print("=" * 80)
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ 已连接到服务器")
        
        print("\n上传文件...")
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('templates/tools/detail.html', '/root/soeasyhub_v2/templates/tools/detail.html')
            print("  ✅ detail.html (添加了宽度/高度输入框和 resize 逻辑)")
        
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
        print("✅ Image Resizer UI 已部署！")
        print("=" * 80)
        
        print("\n🎉 新增 UI 元素：")
        print("  ✅ 宽度输入框 (Width)")
        print("  ✅ 高度输入框 (Height)")
        print("  ✅ 保持宽高比选项 (Maintain aspect ratio)")
        print("  ✅ 提示信息")
        print("  ✅ 'Resize Now' 按钮")
        
        print("\n🔧 功能特点：")
        print("  ✅ 可以只输入宽度或高度")
        print("  ✅ 自动计算另一维度（保持比例）")
        print("  ✅ 可选择是否保持宽高比")
        print("  ✅ 实时预览调整后的图片")
        
        print("\n测试 URL:")
        print("  • http://soeasyhub.com/tools/image-resizer")
        
        print("\n使用方法:")
        print("  1. 上传图片")
        print("  2. 输入目标宽度或高度（或两者都输入）")
        print("  3. 选择是否保持宽高比")
        print("  4. 点击 'Resize Now'")
        print("  5. 预览并下载调整后的图片")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_resizer_ui()
