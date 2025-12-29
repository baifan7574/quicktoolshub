import paramiko

def check_pdf_tools_on_server():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    # 查看服务器上的 pdf_tools.py 文件
    cmd = "head -80 /root/soeasyhub_v2/utils/pdf_tools.py"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    output = stdout.read().decode()
    print("Server pdf_tools.py content:")
    print("="*80)
    print(output)
    
    ssh.close()

if __name__ == "__main__":
    check_pdf_tools_on_server()
