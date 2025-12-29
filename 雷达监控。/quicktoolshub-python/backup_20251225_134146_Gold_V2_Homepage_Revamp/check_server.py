import paramiko
import time

def check_and_restart_server():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    print("检查并重启服务器...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ 已连接到服务器")
        
        # 检查服务状态
        print("\n检查服务状态...")
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
        output = stdout.read().decode()
        
        if output:
            print("✅ Gunicorn 正在运行")
            print(output[:200])
        else:
            print("❌ Gunicorn 未运行")
        
        # 检查错误日志
        print("\n检查错误日志...")
        stdin, stdout, stderr = ssh.exec_command("cd /root/soeasyhub_v2 && tail -50 gunicorn.log")
        log_output = stdout.read().decode()
        print("最近的日志：")
        print(log_output[-500:] if len(log_output) > 500 else log_output)
        
        # 强制重启
        print("\n强制重启服务...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(3)
        
        # 启动服务
        ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
        time.sleep(3)
        
        # 再次检查
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
        output = stdout.read().decode()
        
        if output:
            print("\n✅ 服务已成功重启")
            print(output[:200])
        else:
            print("\n❌ 服务重启失败")
            
            # 尝试查看启动错误
            stdin, stdout, stderr = ssh.exec_command("cd /root/soeasyhub_v2 && tail -20 gunicorn.log")
            error_log = stdout.read().decode()
            print("\n启动错误日志：")
            print(error_log)
        
        # 测试 HTTP 响应
        print("\n测试 HTTP 响应...")
        stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:9999/ | head -20")
        http_response = stdout.read().decode()
        
        if "SoEasyHub" in http_response:
            print("✅ HTTP 响应正常")
        else:
            print("❌ HTTP 响应异常")
            print(http_response[:200])
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()

if __name__ == "__main__":
    check_and_restart_server()
