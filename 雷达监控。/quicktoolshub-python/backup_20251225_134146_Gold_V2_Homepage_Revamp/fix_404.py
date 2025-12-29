"""
在 tools.py 添加 JSON Formatter 定义
"""
import paramiko
from scp import SCPClient
import time

def add_tool_definition():
    print("添加 JSON Formatter 工具定义...")
    
    # 读取本地刚下载的 tools_check.py
    with open('tools_check.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 定义新工具
    json_tool = """
    {
        "slug": "json-formatter",
        "name": "JSON Formatter",
        "description": "Format, validate, and beautify JSON data. Perfect for developers and API testing.",
        "icon": "code",
        "category": "Developer Tools",
        "premium": False
    },"""
    
    # 找到 TOOLS 列表的开始
    # TOOLS = [
    if "TOOLS = [" in content:
        # 在列表开头添加（或者其他合适位置）
        # 我们找 "TOOLS = [" 替换为 "TOOLS = [" + json_tool
        new_content = content.replace("TOOLS = [", "TOOLS = [" + json_tool)
        
        with open('tools_fixed.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print("✅ 已添加工具定义")
        
        # 上传并重启
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
        
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('tools_fixed.py', '/root/soeasyhub_v2/routes/tools.py')
            print("✅ tools.py 已上传")
            
        print("🔄 重启服务...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(2)
        ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
        time.sleep(5)
        
        # 验证
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
        if stdout.read().decode():
            print("✅ 服务启动成功！")
            print("这次真的应该好了！访问: http://soeasyhub.com/tools/json-formatter")
        else:
            print("❌ 服务启动失败")
            
        ssh.close()
    else:
        print("❌ 找不到 TOOLS 列表定义，脚本无法自动修复")

if __name__ == "__main__":
    add_tool_definition()
