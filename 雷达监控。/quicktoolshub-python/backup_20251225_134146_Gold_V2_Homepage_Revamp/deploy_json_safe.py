"""
重新部署 JSON Formatter (安全版)
功能：
1. 安全地注入 SEO 内容到 detail.html (确保语法正确)
2. 注入 JS 逻辑
3. 注入博客文章
4. 重启服务
"""
import sys
sys.path.append('.')
# 导入之前生成的内容
from json_formatter_complete import JSON_FORMATTER_JS, JSON_FORMATTER_SEO, JSON_FORMATTER_BLOG
import paramiko
from scp import SCPClient
import time

def safe_deploy():
    print("🚀 开始部署 JSON Formatter (安全版)...")
    
    # 建立连接
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    print("✅ 已连接服务器")
    
    # ---------------------------------------------------------
    # 1. 处理 detail.html
    # ---------------------------------------------------------
    print("\n📄 处理 detail.html...")
    
    # 下载最新文件
    with SCPClient(ssh.get_transport()) as scp:
        scp.get('/root/soeasyhub_v2/templates/tools/detail.html', 'detail_latest.html')
    
    with open('detail_latest.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # A. 注入 SEO 内容 (独立 IF 块，最安全)
    # 找到 Background Remover 的开始位置
    target_str = "{% if 'background' in tool.slug %}"
    
    if target_str in content and "JSON Formatter Online Free" not in content:
        # 构造完整且闭合的代码块
        new_block = f"""
        {{% if 'json' in tool.slug and 'formatter' in tool.slug %}}
        {JSON_FORMATTER_SEO}
        {{% endif %}}

        """
        # 插入到 target_str 之前
        content = content.replace(target_str, new_block + target_str)
        print("✅ SEO 内容已注入 (独立代码块)")
    else:
        print("⚠️ SEO 内容可能已存在或找不到插入点")

    # B. 注入 JS 逻辑
    js_marker = "</script>\n</body>"
    if js_marker in content and "JSON.parse(jsonText)" not in content:
        content = content.replace(js_marker, f"\n{JSON_FORMATTER_JS}\n{js_marker}")
        print("✅ JS 逻辑已注入")
    else:
        print("⚠️ JS 逻辑可能已存在")

    # 保存 detail.html
    with open('detail_latest.html', 'w', encoding='utf-8') as f:
        f.write(content)

    # ---------------------------------------------------------
    # 2. 处理 blog.py
    # ---------------------------------------------------------
    print("\n📝 处理 blog.py...")
    
    with SCPClient(ssh.get_transport()) as scp:
        scp.get('/root/soeasyhub_v2/routes/blog.py', 'blog_latest.py')
    
    with open('blog_latest.py', 'r', encoding='utf-8') as f:
        blog_content = f.read()

    # 检查是否已存在
    if "json-formatter-online-free-guide" not in blog_content:
        # 构造文章字典
        # 使用 repr() 来安全处理字符串，避免转义问题，然后去掉首尾引号
        # 但为了格式整洁，我们手动构造
        
        # 替换 content 中的三引号，防止冲突
        safe_blog_body = JSON_FORMATTER_BLOG.replace('"""', '\\"\\"\\"')
        
        new_article = f'''    {{
        "slug": "json-formatter-online-free-guide",
        "title": "JSON Formatter Online Free: Complete Guide to Validate and Beautify JSON 2025",
        "description": "Learn how to format JSON online free with validation and error reporting.",
        "keywords": "JSON formatter online free, JSON validator, JSON beautifier",
        "date": "2025-12-23",
        "category": "Developer Tools",
        "tool_name": "JSON Formatter",
        "tool_slug": "json-formatter",
        "excerpt": "Format and validate JSON online with our free JSON formatter tool.",
        "content": """{safe_blog_body}""",
        "related_articles": []
    }},
'''
        # 插入到 ARTICLES 列表末尾 (找到最后一个 ']')
        last_bracket = blog_content.rfind(']')
        if last_bracket != -1:
            blog_content = blog_content[:last_bracket] + new_article + blog_content[last_bracket:]
            print("✅ 博客文章已注入")
        
        with open('blog_latest.py', 'w', encoding='utf-8') as f:
            f.write(blog_content)
    else:
        print("⚠️ 博客文章已存在")

    # ---------------------------------------------------------
    # 3. 上传与重启
    # ---------------------------------------------------------
    print("\n📤 上传文件...")
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('detail_latest.html', '/root/soeasyhub_v2/templates/tools/detail.html')
        scp.put('blog_latest.py', '/root/soeasyhub_v2/routes/blog.py')
    print("✅ 文件已上传")

    print("\n🔄 重启服务...")
    ssh.exec_command("pkill -9 gunicorn || true")
    time.sleep(2)
    # 使用 nohup 启动并确保不挂起
    ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
    time.sleep(5) # 等待启动

    # 检查状态
    stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
    result = stdout.read().decode()
    if result:
        print(f"✅ 服务启动成功!\n{result}")
    else:
        print("❌ 服务启动失败，请检查日志")
        stdin, stdout, stderr = ssh.exec_command("tail -n 20 /root/soeasyhub_v2/gunicorn.log")
        print(stdout.read().decode())

    ssh.close()
    print("\n✨ 部署完成！请访问 http://soeasyhub.com/tools/json-formatter")

if __name__ == "__main__":
    try:
        safe_deploy()
    except Exception as e:
        print(f"❌ 脚本执行出错: {e}")
        import traceback
        traceback.print_exc()
