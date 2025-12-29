import paramiko

def check_server_file():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    print("检查服务器上的 detail.html...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ 已连接到服务器")
        
        # 检查按钮代码
        stdin, stdout, stderr = ssh.exec_command("grep -A 10 'process-btn' /root/soeasyhub_v2/templates/tools/detail.html | head -20")
        output = stdout.read().decode()
        
        print("\n服务器上的按钮代码：")
        print(output)
        
        if "Learn More" in output:
            print("\n❌ 错误：服务器上的文件仍然包含错误的博客链接！")
            print("需要重新上传正确的文件")
        else:
            print("\n✅ 服务器上的文件看起来正确")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    check_server_file()
