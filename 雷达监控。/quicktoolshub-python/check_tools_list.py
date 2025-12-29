"""
检查 tools.py 里的工具定义
"""
import paramiko
from scp import SCPClient

def check_tools():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    print("下载 tools.py...")
    with SCPClient(ssh.get_transport()) as scp:
        scp.get('/root/soeasyhub_v2/routes/tools.py', 'tools_check.py')
        
    with open('tools_check.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
    print("\n检查 json-formatter 是否在工具列表中...")
    if "json-formatter" in content:
        print("✅ 找到了 json-formatter")
        # 打印相关行
        for line in content.split('\n'):
            if "json-formatter" in line:
                print(f"  {line.strip()}")
    else:
        print("❌ 没找到 json-formatter！这就是 404 的原因！")
        
    ssh.close()

if __name__ == "__main__":
    check_tools()
