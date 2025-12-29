#!/usr/bin/env python3
"""
稳定部署脚本 - 经过验证，不要修改
端口：9999 (与Nginx配置一致)
"""
import paramiko
from scp import SCPClient
import subprocess
import time
import os

HOST = "43.130.229.184"
USER = "root"
PW = "baifan100100"
REMOTE_BASE = "/root/soeasyhub_v2"
PORT = 9999  # 固定端口，不要修改

def check_syntax():
    """语法检查"""
    print("🔍 检查语法...")
    files = ['tools_new.py', 'blog_final.py']
    for f in files:
        if not os.path.exists(f):
            print(f"⚠️  {f} 不存在，跳过")
            continue
        result = subprocess.run(['python', '-m', 'py_compile', f], capture_output=True)
        if result.returncode != 0:
            print(f"❌ {f} 语法错误")
            print(result.stderr.decode())
            return False
        print(f"✓ {f}")
    return True

def deploy():
    """执行部署"""
    print("\n📤 上传文件...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password=PW)
    
    with SCPClient(ssh.get_transport()) as scp:
        # 只上传我们修改的3个文件
        if os.path.exists('tools_new.py'):
            scp.put('tools_new.py', f'{REMOTE_BASE}/routes/tools.py')
            print("✓ routes/tools.py")
        
        if os.path.exists('blog_final.py'):
            scp.put('blog_final.py', f'{REMOTE_BASE}/routes/blog.py')
            print("✓ routes/blog.py")

        if os.path.exists('detail_new.html'):
            scp.put('detail_new.html', f'{REMOTE_BASE}/templates/tools/detail.html')
            print("✓ templates/tools/detail.html")

        # 2025-12-25 Homepage Overhaul Update
        if os.path.exists('app.py'):
            scp.put('app.py', f'{REMOTE_BASE}/app.py')
            print("✓ app.py (Controller Updated)")
            
        if os.path.exists('templates/index.html'):
            scp.put('templates/index.html', f'{REMOTE_BASE}/templates/index.html')
            print("✓ templates/index.html (Homepage Updated)")
        
        # FIX: Ensure wish_wall.html is uploaded
        if os.path.exists(r'templates\pages\wish_wall.html') or os.path.exists('templates/pages/wish_wall.html'):
            local_path = r'templates\pages\wish_wall.html' if os.path.exists(r'templates\pages\wish_wall.html') else 'templates/pages/wish_wall.html'
            ssh.exec_command(f'mkdir -p {REMOTE_BASE}/templates/pages')
            scp.put(local_path, f'{REMOTE_BASE}/templates/pages/wish_wall.html')
            print("✓ templates/pages/wish_wall.html")
    
    print("\n🔄 重启服务...")
    # 停止PM2
    ssh.exec_command('pm2 stop all 2>/dev/null || true')
    # 杀掉所有Gunicorn
    ssh.exec_command('pkill -9 -f gunicorn 2>/dev/null || true')
    time.sleep(2)
    
    # 启动正确端口的Gunicorn
    cmd = f"cd {REMOTE_BASE} && nohup python3 -m gunicorn -w 4 -b 127.0.0.1:{PORT} app:app --preload > gunicorn.log 2>&1 &"
    ssh.exec_command(cmd)
    time.sleep(3)
    
    print("\n🔍 验证...")
    _, stdout, _ = ssh.exec_command(f'curl -s -o /dev/null -w "%{{http_code}}" http://localhost:{PORT}/')
    status = stdout.read().decode().strip()
    
    if status == "200":
        print(f"✅ 部署成功! HTTP Status: {status}")
        ssh.close()
        return True
    else:
        print(f"❌ 部署失败! HTTP Status: {status}")
        ssh.close()
        return False

def main():
    print("=" * 50)
    print("  稳定部署脚本 v1.0")
    print("=" * 50)
    
    if not check_syntax():
        print("\n❌ 语法检查失败，中止部署")
        return 1
    
    if deploy():
        print("\n✅ 部署完成!")
        return 0
    else:
        print("\n❌ 部署失败!")
        return 1

if __name__ == "__main__":
    exit(main())
