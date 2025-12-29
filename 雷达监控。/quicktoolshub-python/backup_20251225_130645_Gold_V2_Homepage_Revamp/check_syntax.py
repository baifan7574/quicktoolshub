"""
验证服务器上的 Python 文件语法
"""
import paramiko

def check_syntax():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    print("正在检查 blog.py 语法...")
    stdin, stdout, stderr = ssh.exec_command("python3 -m py_compile /root/soeasyhub_v2/routes/blog.py")
    err = stderr.read().decode()
    if err:
        print("❌ blog.py 有语法错误:")
        print(err)
    else:
        print("✅ blog.py 语法正确")

    print("\n正在检查 tools.py 语法...")
    stdin, stdout, stderr = ssh.exec_command("python3 -m py_compile /root/soeasyhub_v2/routes/tools.py")
    err = stderr.read().decode()
    if err:
        print("❌ tools.py 有语法错误:")
        print(err)
    else:
        print("✅ tools.py 语法正确")
        
    print("\n正在检查 app.py 语法...")
    stdin, stdout, stderr = ssh.exec_command("python3 -m py_compile /root/soeasyhub_v2/app.py")
    err = stderr.read().decode()
    if err:
        print("❌ app.py 有语法错误:")
        print(err)
    else:
        print("✅ app.py 语法正确")

    ssh.close()

if __name__ == "__main__":
    check_syntax()
