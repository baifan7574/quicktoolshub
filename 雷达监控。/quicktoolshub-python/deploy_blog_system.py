import paramiko
from scp import SCPClient
import time

def deploy_blog_system():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    print("部署博客系统...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ 已连接到服务器")
        
        print("\n上传文件...")
        with SCPClient(ssh.get_transport()) as scp:
            # 上传博客模板
            scp.put('templates/blog/index.html', '/root/soeasyhub_v2/templates/blog/index.html')
            print("  ✅ blog/index.html")
            
            scp.put('templates/blog/article.html', '/root/soeasyhub_v2/templates/blog/article.html')
            print("  ✅ blog/article.html")
            
            # 上传博客路由
            scp.put('routes/blog.py', '/root/soeasyhub_v2/routes/blog.py')
            print("  ✅ routes/blog.py")
            
            # 上传更新的 base.html
            scp.put('templates/base.html', '/root/soeasyhub_v2/templates/base.html')
            print("  ✅ base.html（导航栏已更新）")
        
        print("\n重启服务...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(2)
        ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
        
        print("\n✅ 博客系统部署完成！")
        print("\n现在您可以访问：")
        print("  📝 博客首页: http://soeasyhub.com/blog")
        print("  📄 示例文章: http://soeasyhub.com/blog/how-to-compress-pdf-online-free")
        print("\n导航栏已更新：")
        print("  ✅ Tool Hub")
        print("  ✅ Blog ← 新增！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_blog_system()
