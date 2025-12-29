"""
Force clean install of tools.py
"""
import paramiko
from scp import SCPClient
import time

def clean_install():
    print("开始干净安装 tools.py...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    # 1. 停止服务
    print("停止服务...")
    ssh.exec_command("pkill -9 gunicorn")
    time.sleep(2)
    
    # 2. 删除旧文件 (备份一下比较好，但为了确保，我们直接覆盖)
    print("上传新文件...")
    with SCPClient(ssh.get_transport()) as scp:
        # 使用本地的 tools_complete.py (之前编写的包含硬编码逻辑的完整文件)
        scp.put('tools_complete.py', '/root/soeasyhub_v2/routes/tools.py')
        # 还要确保 detail.html 是好的 (安全起见)
        scp.put('detail_latest.html', '/root/soeasyhub_v2/templates/tools/detail.html')
        
    print("文件已替换")
    
    # 3. 编译验证 (防止上传坏文件)
    stdin, stdout, stderr = ssh.exec_command("python3 -m py_compile /root/soeasyhub_v2/routes/tools.py")
    err = stderr.read().decode()
    if err:
        print("❌ 上传的文件有语法错误！终止启动。")
        print(err)
        return

    # 4. 启动服务
    print("启动服务...")
    # 使用完整的启动命令，指定路径
    cmd = "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ssh.exec_command(cmd)
    time.sleep(5)
    
    # 5. 验证进程
    stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
    ps = stdout.read().decode()
    if ps:
        print("✅ 服务已启动")
        # 6. 本地验证 404
        stdin, stdout, stderr = ssh.exec_command("curl -I http://127.0.0.1:9999/tools/json-formatter")
        resp = stdout.read().decode()
        print("\n服务器本地测试结果:")
        print(resp)
        if "200 OK" in resp:
            print("🎉 成功！就是它了！")
        else:
            print("❌ 依然失败... 返回码不是 200")
            
    else:
        print("❌ 服务启动失败，查看日志:")
        stdin, stdout, stderr = ssh.exec_command("tail -n 20 /root/soeasyhub_v2/gunicorn.log")
        print(stdout.read().decode())
        
    ssh.close()

if __name__ == "__main__":
    clean_install()
