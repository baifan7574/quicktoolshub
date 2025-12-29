"""
检查服务器错误日志
"""
import paramiko

def check_error():
    print("检查服务器错误...")
    
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ 已连接\n")
        
        # 检查 Gunicorn 日志
        print("=" * 80)
        print("Gunicorn 日志（最后 50 行）：")
        print("=" * 80)
        stdin, stdout, stderr = ssh.exec_command("cd /root/soeasyhub_v2 && tail -50 gunicorn.log")
        log = stdout.read().decode()
        print(log)
        
        # 检查 Python 语法
        print("\n" + "=" * 80)
        print("检查 detail.html 模板语法：")
        print("=" * 80)
        stdin, stdout, stderr = ssh.exec_command("cd /root/soeasyhub_v2 && python3 -c 'from flask import Flask; app = Flask(__name__); app.config[\"TEMPLATES_AUTO_RELOAD\"] = True; from jinja2 import Environment, FileSystemLoader; env = Environment(loader=FileSystemLoader(\"templates\")); env.get_template(\"tools/detail.html\")'")
        error = stderr.read().decode()
        if error:
            print("❌ 模板错误:")
            print(error)
        else:
            print("✅ 模板语法正确")
        
        # 检查进程
        print("\n" + "=" * 80)
        print("Gunicorn 进程状态：")
        print("=" * 80)
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
        ps = stdout.read().decode()
        if ps:
            print("✅ 进程运行中:")
            print(ps)
        else:
            print("❌ 进程未运行")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    check_error()
