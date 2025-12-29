"""
修复 detail.html - 删除重复的 JSON Formatter 并添加 endif
"""
import paramiko
from scp import SCPClient
import time

# 读取服务器文件
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)

with SCPClient(ssh.get_transport()) as scp:
    scp.get('/root/soeasyhub_v2/templates/tools/detail.html', 'detail_fix.html')

print("已下载文件")

# 读取并修复
with open('detail_fix.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到并删除第一个 JSON Formatter (行 372)
# 找到并为第二个添加 endif (行 585)

new_lines = []
skip_until = -1
json_if_count = 0

for i, line in enumerate(lines):
    # 如果遇到 JSON Formatter 的 if
    if "{% if 'json' in tool.slug and 'formatter' in tool.slug %}" in line:
        json_if_count += 1
        if json_if_count == 1:
            # 第一个：跳过它和它后面的内容，直到下一个 {% if
            skip_until = i
            print(f"跳过第一个 JSON Formatter (行 {i+1})")
            continue
        else:
            # 第二个：保留，但需要添加 endif
            new_lines.append(line)
    elif skip_until >= 0 and i > skip_until:
        # 正在跳过第一个 JSON Formatter 的内容
        if "{% if 'background' in tool.slug %}" in line:
            # 遇到下一个 if，停止跳过
            skip_until = -1
            new_lines.append(line)
        # 否则继续跳过
    else:
        new_lines.append(line)

# 现在需要在第二个 JSON Formatter 后面添加 endif
# 找到 "{% if 'background' in tool.slug %}" 并在它前面添加 endif
final_lines = []
for i, line in enumerate(new_lines):
    if "{% if 'background' in tool.slug %}" in line and json_if_count > 0:
        # 在这之前添加 endif
        final_lines.append("        {% endif %}\n\n")
        json_if_count = 0  # 只添加一次
    final_lines.append(line)

# 保存
with open('detail_fix.html', 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print("已修复文件")

# 上传
with SCPClient(ssh.get_transport()) as scp:
    scp.put('detail_fix.html', '/root/soeasyhub_v2/templates/tools/detail.html')

print("已上传")

# 重启
ssh.exec_command("pkill -9 gunicorn || true")
time.sleep(3)
ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
time.sleep(3)

print("✅ 已修复并重启！")
print("现在访问: http://soeasyhub.com/tools/json-formatter")

ssh.close()
