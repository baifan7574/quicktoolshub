"""
最简单的解决方案：
1. 从服务器获取当前文件
2. 删除所有 JSON Formatter 相关内容
3. 上传干净版本
4. 重启服务
"""
import paramiko
from scp import SCPClient
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)

print("下载文件...")
with SCPClient(ssh.get_transport()) as scp:
    scp.get('/root/soeasyhub_v2/templates/tools/detail.html', 'detail_clean.html')

# 读取并删除所有 JSON Formatter 内容
with open('detail_clean.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 删除所有包含 'json' 和 'formatter' 的 if 语句块
# 简单粗暴：找到这些行并删除
lines = content.split('\n')
new_lines = []
skip = False

for line in lines:
    # 如果遇到 JSON Formatter 的 if
    if "{% if 'json' in tool.slug and 'formatter' in tool.slug %}" in line:
        skip = True
        print(f"开始跳过 JSON Formatter 块")
        continue
    
    # 如果在跳过模式，寻找下一个 {% if 或 {% elif
    if skip:
        if ("{% if" in line and "'json'" not in line) or "{% elif" in line:
            skip = False
            print(f"停止跳过，遇到: {line.strip()[:50]}")
            new_lines.append(line)
        # 继续跳过
        continue
    
    new_lines.append(line)

# 保存
content = '\n'.join(new_lines)
with open('detail_clean.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("已删除 JSON Formatter 内容")

# 上传
with SCPClient(ssh.get_transport()) as scp:
    scp.put('detail_clean.html', '/root/soeasyhub_v2/templates/tools/detail.html')

print("已上传干净版本")

# 重启
ssh.exec_command("pkill -9 gunicorn || true")
time.sleep(3)
ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
time.sleep(3)

print("✅ 已恢复干净版本并重启")
print("现在网站应该可以正常访问了")
print("\nJSON Formatter 功能已暂时移除，等待正确实现")

ssh.close()
