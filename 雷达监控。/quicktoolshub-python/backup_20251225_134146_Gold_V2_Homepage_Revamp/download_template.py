"""
从服务器下载 detail.html 查看问题
"""
import paramiko
from scp import SCPClient

def download_and_check():
    print("从服务器下载 detail.html...")
    
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ 已连接")
        
        # 下载文件
        with SCPClient(ssh.get_transport()) as scp:
            scp.get('/root/soeasyhub_v2/templates/tools/detail.html', 'detail_from_server.html')
            print("✅ 已下载到 detail_from_server.html")
        
        # 检查 if/endif 配对
        with open('detail_from_server.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 统计 if 和 endif
        if_count = content.count('{% if')
        elif_count = content.count('{% elif')
        endif_count = content.count('{% endif %}')
        
        print("\n统计:")
        print("  {%% if ... %%}: {}".format(if_count))
        print("  {%% elif ... %%}: {}".format(elif_count))
        print("  {%% endif %%}: {}".format(endif_count))
        print("\n需要的 endif 数量: {}".format(if_count))
        print("实际的 endif 数量: {}".format(endif_count))
        print("缺少: {} 个 endif".format(if_count - endif_count))
        
        # 找到所有 if 语句的位置
        print("\n所有 if 语句:")
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if '{% if' in line or '{% elif' in line or '{% endif %}' in line:
                print(f"  行 {i}: {line.strip()[:80]}")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    download_and_check()
