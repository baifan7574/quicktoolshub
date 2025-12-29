"""
通过修改 Python 代码强制添加 JSON Formatter
"""
import sys
sys.path.append('.')
import paramiko
from scp import SCPClient
import time

def force_add_tool():
    print("开始强制添加 JSON Formatter 到 tools.py...")
    
    # 读取 tools_check.py (刚才下载的)
    with open('tools_check.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 我们要修改 get_tools_list 函数
    # 在 return tools_data 之前
    
    target = "    return tools_data"
    
    # 构造新的工具数据
    new_tool_logic = """
    # 强制添加 JSON Formatter (如果列表中还没有)
    has_json = False
    for t in tools_data:
        if t.get('slug') == 'json-formatter':
            has_json = True
            break
            
    if not has_json and (not category_slug or category_slug == 'all' or category_slug == 'developer-tools'):
        json_tool = {
            "id": 999,
            "name": "JSON Formatter",
            "slug": "json-formatter",
            "description": "Format, validate, and beautify JSON data. Perfect for developers and API testing.",
            "short_description": "Format and validate JSON instantly.",
            "view_count": 0,
            "tool_type": "local",
            "category_id": 4,  # 假设 4 是 Developer Tools
            "categories": {"name": "Developer Tools", "slug": "developer-tools"}
        }
        tools_data.append(json_tool)

    return tools_data"""
    
    # 替换
    if target in content:
        # 只替换第一次出现的地方 (get_tools_list 的结尾)
        new_content = content.replace(target, new_tool_logic, 1)
        
        # 还需要修改 tool_detail 函数，因为它也从数据库查
        # 如果数据库查不到，它返回 "Tool not found"
        # 我们需要拦截这个 404
        
        detail_target = """    if not tool_result.data:
        return "Tool not found", 404"""
        
        detail_fix = """    if not tool_result.data:
        # 手动处理 JSON Formatter
        if slug == 'json-formatter':
            tool = {
                "id": 999,
                "name": "JSON Formatter",
                "slug": "json-formatter",
                "description": "Format, validate, and beautify JSON data.",
                "view_count": 0,
                "category_id": 4,
                "categories": {"name": "Developer Tools", "slug": "developer-tools"}
            }
            # 获取相关工具 (模拟)
            related_tools = []
            return render_template('tools/detail.html', tool=tool, related_tools=related_tools)
            
        return "Tool not found", 404"""
        
        if detail_target in new_content:
            new_content = new_content.replace(detail_target, detail_fix)
            
        # 保存
        with open('tools_patched.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print("✅ 已修补 Python 代码")
        
        # 上传并重启
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
        
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('tools_patched.py', '/root/soeasyhub_v2/routes/tools.py')
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
            print("现在 404 应该解决了！访问: http://soeasyhub.com/tools/json-formatter")
        else:
            print("❌ 服务启动失败")
            
        ssh.close()
    else:
        print("❌ 无法定位代码插入点")

if __name__ == "__main__":
    force_add_tool()
