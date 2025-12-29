import paramiko

def check_server_error():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    print("检查服务器错误...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ 已连接到服务器")
        
        # 检查 gunicorn 进程
        print("\n检查 Gunicorn 进程...")
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
        output = stdout.read().decode()
        
        if output:
            print("✅ Gunicorn 正在运行")
        else:
            print("❌ Gunicorn 未运行")
        
        # 检查错误日志
        print("\n检查错误日志（最后 50 行）...")
        stdin, stdout, stderr = ssh.exec_command("cd /root/soeasyhub_v2 && tail -50 gunicorn.log")
        log_output = stdout.read().decode()
        print(log_output)
        
        # 尝试手动启动看错误
        print("\n尝试手动启动 Gunicorn...")
        stdin, stdout, stderr = ssh.exec_command("cd /root/soeasyhub_v2 && python3 -c 'import routes.blog'")
        error_output = stderr.read().decode()
        
        if error_output:
            print("\n❌ Python 错误：")
            print(error_output)
        else:
            print("✅ blog.py 导入成功")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()

if __name__ == "__main__":
    check_server_error()
