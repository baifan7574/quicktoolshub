"""
修复 detail.html 模板语法错误
问题：添加了 {% if %} 但没有 {% endif %}
"""
import paramiko
from scp import SCPClient
import time

def fix_template():
    print("修复模板语法错误...")
    
    # 读取文件
    with open('templates/tools/detail.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到我们添加的 JSON Formatter 部分
    # 需要在它后面添加 {% endif %}
    
    # 查找 JSON Formatter 的 if 语句
    json_if = "{% if 'json' in tool.slug and 'formatter' in tool.slug %}"
    
    if json_if in content:
        # 找到这个 if 之后的下一个 {% if
        start_pos = content.find(json_if)
        next_if_pos = content.find("{% if 'background' in tool.slug %}", start_pos + len(json_if))
        
        if next_if_pos != -1:
            # 在下一个 if 之前插入 {% endif %}
            content = content[:next_if_pos] + "\n        {% endif %}\n\n        " + content[next_if_pos:]
            print("✅ 已添加缺失的 {% endif %}")
    
    # 保存
    with open('templates/tools/detail.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 部署
    print("\n部署到服务器...")
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ 已连接")
        
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('templates/tools/detail.html', '/root/soeasyhub_v2/templates/tools/detail.html')
            print("✅ 已上传")
        
        # 验证模板语法
        print("\n验证模板语法...")
        stdin, stdout, stderr = ssh.exec_command("cd /root/soeasyhub_v2 && python3 -c 'from jinja2 import Environment, FileSystemLoader; env = Environment(loader=FileSystemLoader(\"templates\")); env.get_template(\"tools/detail.html\")'")
        error = stderr.read().decode()
        
        if error:
            print("❌ 模板仍有错误:")
            print(error)
            return
        else:
            print("✅ 模板语法正确")
        
        print("\n重启服务...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(3)
        ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
        time.sleep(3)
        
        print("✅ 服务已重启")
        print("\n现在可以访问: http://soeasyhub.com/tools/json-formatter")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    fix_template()
