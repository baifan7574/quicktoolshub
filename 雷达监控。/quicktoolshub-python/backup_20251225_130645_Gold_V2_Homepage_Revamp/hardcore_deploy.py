import paramiko
import time

def hardcore_restart():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password)
        print("🚀 正在对服务器执行“外科手术式”重启...")
        
        # 1. 直接通过端口杀掉所有进程
        print("🔪 正在清理 9999 端口上的旧势力...")
        ssh.exec_command("fuser -k 9999/tcp")
        time.sleep(2)
        
        # 2. 再次通过名字补刀
        ssh.exec_command("pkill -9 gunicorn")
        ssh.exec_command("pkill -9 python3") # 稍微危险，但在该环境下可行
        time.sleep(1)
        
        # 3. 验证端口是否已空
        stdin, stdout, stderr = ssh.exec_command("lsof -i :9999")
        if not stdout.read().decode():
            print("✅ 9999 端口已彻底排空。")
        else:
            print("⚠️ 警告：9999 端口仍被占用，尝试强力清除...")
            ssh.exec_command("kill -9 $(lsof -t -i:9999)")
        
        # 4. 重新启动
        print("🏗️ 正在重新挂载「黄金版」首页系统...")
        cmd = "cd /root/soeasyhub_v2 && nohup python3 -m gunicorn -w 4 -b 127.0.0.1:9999 app:app --preload > gunicorn_final.log 2>&1 &"
        ssh.exec_command(cmd)
        time.sleep(3)
        
        # 5. 最终内部校验
        stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:9999 | grep 'Free Online Tools'")
        result = stdout.read().decode()
        if "Free Online Tools" in result:
            print("\n" + "★"*30)
            print("🎉 内部校验成功！服务器输出已变更为新版。")
            print("★"*30)
        else:
            print("\n❌ 脚本内部校验失败，可能还是旧代码，详情：")
            print(result[:100])
            
    except Exception as e:
        print(f"❌ 发生致命错误: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    hardcore_restart()
