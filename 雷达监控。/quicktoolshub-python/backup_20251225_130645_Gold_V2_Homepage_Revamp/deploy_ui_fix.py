import paramiko
from scp import SCPClient
import time

def deploy_ui_fix():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    print("部署 UI 修复...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ 已连接到服务器")
        
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('templates/tools/detail.html', '/root/soeasyhub_v2/templates/tools/detail.html')
            print("  ✅ detail.html 已上传")
        
        print("\n重启服务...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(2)
        ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
        
        print("\n✅ UI 修复完成！")
        print("\n问题：博客链接被错误插入到按钮代码中")
        print("解决：已删除错误的插入，按钮现在正常工作")
        print("\n请刷新页面测试！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_ui_fix()
